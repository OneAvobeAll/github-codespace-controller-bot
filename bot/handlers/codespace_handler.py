"""
Codespace management handlers
"""
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from github_api.github_manager import GitHubManager
from database.db import db

logger = logging.getLogger(__name__)


async def start_codespace(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start a new Codespace for an application"""
    query = update.callback_query
    await query.answer()
    
    app_id = query.data.split('_')[2]
    app = await db.get_application(app_id)
    user = await db.get_user(update.effective_user.id)
    
    if not user.get('github_tokens'):
        await query.edit_message_text(
            text="❌ No GitHub API token configured.\n\nPlease go to Settings and add your GitHub API token first."
        )
        return
    
    # Use the active token
    active_token = next(
        (t['token'] for t in user['github_tokens'] if t.get('is_active')),
        user['github_tokens'][0]['token'] if user['github_tokens'] else None
    )
    
    if not active_token:
        await query.edit_message_text(
            text="❌ No active GitHub API token found."
        )
        return
    
    await query.edit_message_text(
        text=f"⏳ Starting Codespace for **{app['name']}**...\n\nThis may take a minute..."
    )
    
    try:
        # Fork and create Codespace
        success, result = await _fork_and_create_codespace(
            app_id, 
            active_token,
            app.get('repo_url')
        )
        
        if not success:
            await query.edit_message_text(
                text=f"❌ Error: {result}"
            )
            return
        
        # Get environment variables and build/start commands
        env_vars = app.get('env_vars', {})
        build_cmd = app.get('build_command')
        start_cmd = app.get('start_command')
        
        message = f"""✅ **Codespace Started!**

**Codespace Details:**
- Name: {result['codespace_name']}
- URL: [Open in Browser]({result['codespace_url']})
- Status: Running
- CPU: 4-Core
- RAM: 16GB
- Storage: 32GB

**Configuration:**
- Repository: {app.get('repo_url')}
- Build Command: {build_cmd or 'Not set'}
- Start Command: {start_cmd or 'Not set'}
- Docker: {'Enabled' if app.get('docker_enabled') else 'Disabled'}
- Environment Variables: {len(env_vars)} set
"""
        
        if app.get('docker_enabled') or (build_cmd or start_cmd):
            message += "\n⏳ Running build and start commands..."
        
        keyboard = [
            [InlineKeyboardButton("🌐 Open Codespace", url=result['codespace_url'])],
            [InlineKeyboardButton("⏹️ Stop Codespace", callback_data=f"stop_codespace_{app_id}")],
            [InlineKeyboardButton("📊 Check Status", callback_data=f"check_status_{app_id}")],
            [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=message,
            reply_markup=reply_markup,
            disable_web_page_preview=False
        )
    
    except Exception as e:
        logger.error(f"Error starting Codespace: {str(e)}")
        await query.edit_message_text(
            text=f"❌ Error starting Codespace: {str(e)}"
        )


async def stop_codespace(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Stop a running Codespace"""
    query = update.callback_query
    await query.answer()
    
    app_id = query.data.split('_')[2]
    app = await db.get_application(app_id)
    user = await db.get_user(update.effective_user.id)
    
    if not app.get('codespace_id'):
        await query.edit_message_text(
            text="❌ No active Codespace found for this application."
        )
        return
    
    # Get active token
    active_token = next(
        (t['token'] for t in user['github_tokens'] if t.get('is_active')),
        user['github_tokens'][0]['token'] if user['github_tokens'] else None
    )
    
    if not active_token:
        await query.edit_message_text(
            text="❌ No GitHub API token found."
        )
        return
    
    await query.edit_message_text(
        text=f"⏳ Stopping Codespace for **{app['name']}**..."
    )
    
    try:
        gh_manager = GitHubManager(active_token)
        forked_repo = app.get('forked_repo')
        codespace_name = app.get('codespace_name')
        
        # Stop the Codespace
        success = await gh_manager.stop_codespace(forked_repo, codespace_name)
        
        if success:
            await db.update_application(app_id, {'status': 'stopped'})
            
            keyboard = [
                [InlineKeyboardButton("▶️ Start Codespace", callback_data=f"start_codespace_{app_id}")],
                [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                text=f"✅ Codespace stopped successfully.",
                reply_markup=reply_markup
            )
        else:
            await query.edit_message_text(
                text="❌ Failed to stop Codespace."
            )
    
    except Exception as e:
        logger.error(f"Error stopping Codespace: {str(e)}")
        await query.edit_message_text(
            text=f"❌ Error: {str(e)}"
        )


async def check_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Check Codespace status"""
    query = update.callback_query
    await query.answer()
    
    app_id = query.data.split('_')[2]
    app = await db.get_application(app_id)
    user = await db.get_user(update.effective_user.id)
    
    if not app.get('codespace_id'):
        await query.edit_message_text(
            text="❌ No active Codespace found."
        )
        return
    
    # Get active token
    active_token = next(
        (t['token'] for t in user['github_tokens'] if t.get('is_active')),
        user['github_tokens'][0]['token'] if user['github_tokens'] else None
    )
    
    try:
        gh_manager = GitHubManager(active_token)
        forked_repo = app.get('forked_repo')
        codespace_name = app.get('codespace_name')
        
        # Get Codespace status
        codespace = await gh_manager.get_codespace(forked_repo, codespace_name)
        
        status_text = f"""📊 **Codespace Status**

**Application:** {app['name']}
**Codespace:** {codespace_name}
**Status:** {codespace.get('state', 'Unknown')}
**URL:** [Open]({codespace.get('web_url')})
**Created:** {codespace.get('created_at', 'N/A')}
**Last Used:** {codespace.get('last_used_at', 'N/A')}
"""
        
        await query.edit_message_text(text=status_text)
    
    except Exception as e:
        logger.error(f"Error checking status: {str(e)}")
        await query.edit_message_text(
            text=f"❌ Error: {str(e)}"
        )


async def _fork_and_create_codespace(app_id: str, github_token: str, repo_url: str):
    """Fork repository and create Codespace"""
    try:
        gh_manager = GitHubManager(github_token)
        
        # Extract owner and repo
        parts = repo_url.strip('/').split('/')
        owner, repo = parts[-2], parts[-1].replace('.git', '')
        
        # Fork repository
        forked_repo = await gh_manager.fork_repository(owner, repo)
        
        if not forked_repo:
            return False, "Failed to fork repository"
        
        # Create Codespace with 4-core, 16GB, 32GB storage
        codespace = await gh_manager.create_codespace(
            forked_repo['full_name'],
            machine_type='standard_4_core_16gb_32gb'
        )
        
        if not codespace:
            return False, "Failed to create Codespace"
        
        return True, {
            'codespace_url': codespace['web_url'],
            'codespace_name': codespace['name'],
            'codespace_id': codespace['id']
        }
    
    except Exception as e:
        logger.error(f"Error in fork and create: {str(e)}")
        return False, str(e)
