"""
Settings and configuration handlers
"""
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database.db import db

logger = logging.getLogger(__name__)


async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show settings menu"""
    query = update.callback_query if update.callback_query else update
    
    keyboard = [
        [InlineKeyboardButton("🔑 Manage GitHub Tokens", callback_data="manage_tokens")],
        [InlineKeyboardButton("💳 View Billing", callback_data="view_billing")],
        [InlineKeyboardButton("📊 Usage Limits", callback_data="usage_limits")],
        [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    settings_text = """⚙️ **Settings**

Manage your bot settings and preferences.
    """
    
    if hasattr(query, 'edit_message_text'):
        await query.edit_message_text(text=settings_text, reply_markup=reply_markup)
    else:
        await query.message.reply_text(settings_text, reply_markup=reply_markup)


async def manage_tokens(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manage GitHub API tokens"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    user = await db.get_user(user_id)
    tokens = user.get('github_tokens', [])
    
    if not tokens:
        keyboard = [
            [InlineKeyboardButton("➕ Add GitHub Token", callback_data="add_token")],
            [InlineKeyboardButton("⬅️ Back", callback_data="settings")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text="🔑 **GitHub Tokens**\n\nYou haven't added any GitHub API tokens yet.\n\nAdd your token to get started.",
            reply_markup=reply_markup
        )
        return
    
    tokens_text = "🔑 **GitHub Tokens**\n\n"
    buttons = []
    
    for i, token_info in enumerate(tokens, 1):
        token_preview = token_info['token'][:10] + '...' if token_info['token'] else 'Unknown'
        is_active = "✅ Active" if token_info.get('is_active') else "⭕ Inactive"
        
        tokens_text += f"{i}. {token_preview}\n   Status: {is_active}\n\n"
        
        # Add buttons for each token
        if not token_info.get('is_active'):
            buttons.append([InlineKeyboardButton(
                f"Use Token {i}",
                callback_data=f"switch_token_{token_info['_id']}"
            )])
        
        buttons.append([InlineKeyboardButton(
            f"🗑️ Delete Token {i}",
            callback_data=f"delete_token_{token_info['_id']}"
        )])
    
    buttons.append([InlineKeyboardButton("➕ Add New Token", callback_data="add_token")])
    buttons.append([InlineKeyboardButton("⬅️ Back", callback_data="settings")])
    
    reply_markup = InlineKeyboardMarkup(buttons)
    await query.edit_message_text(text=tokens_text, reply_markup=reply_markup)


async def add_token(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Add new GitHub API token"""
    query = update.callback_query
    await query.answer()
    
    context.user_data['action'] = 'add_github_token'
    
    await query.edit_message_text(
        text="🔑 **Add GitHub Token**\n\nSend your GitHub Personal Access Token:\n\n(Get one from: https://github.com/settings/tokens)"
    )


async def view_billing(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View GitHub billing information"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    user = await db.get_user(user_id)
    
    if not user.get('github_tokens'):
        await query.edit_message_text(
            text="❌ No GitHub API token configured.\n\nCannot fetch billing information without a token."
        )
        return
    
    billing_text = """💳 **GitHub Billing**

**Codespace Usage:**
- Hours Used: Calculating...
- Monthly Allowance: 120 hours
- Overage Rate: $0.18/hour

**Storage:**
- Used: Calculating...
- Included: 15 GB/month
- Overage Rate: $0.07/GB

Visit https://github.com/settings/billing for detailed info
    """
    
    keyboard = [
        [InlineKeyboardButton("🔄 Refresh", callback_data="view_billing")],
        [InlineKeyboardButton("⬅️ Back", callback_data="settings")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text=billing_text, reply_markup=reply_markup)


async def usage_limits(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Set usage limits and alerts"""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("⏰ Set Codespace Limit", callback_data="set_codespace_limit")],
        [InlineKeyboardButton("💾 Set Storage Limit", callback_data="set_storage_limit")],
        [InlineKeyboardButton("🔔 Notifications", callback_data="notification_settings")],
        [InlineKeyboardButton("⬅️ Back", callback_data="settings")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    limits_text = """📊 **Usage Limits**

Configure alerts and limits for your Codespace usage:
    """
    
    await query.edit_message_text(text=limits_text, reply_markup=reply_markup)


async def handle_token_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle GitHub token input"""
    user_id = update.effective_user.id
    token = update.message.text.strip()
    
    if context.user_data.get('action') == 'add_github_token':
        # Validate token format (GitHub tokens start with ghp_ or gho_)
        if not (token.startswith('ghp_') or token.startswith('gho_')):
            await update.message.reply_text(
                "❌ Invalid GitHub token format.\n\nToken should start with 'ghp_' or 'gho_'."
            )
            return
        
        # Add token to user
        success = await db.add_github_token(user_id, token)
        
        if success:
            context.user_data['action'] = None
            await update.message.reply_text(
                text="✅ GitHub token added successfully!\n\nToken is now active and ready to use."
            )
        else:
            await update.message.reply_text(
                text="❌ Failed to add token. Please try again."
            )
