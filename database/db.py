"""MongoDB database operations"""
import logging
import uuid
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo import errors
from config import MONGODB_URI, DATABASE_NAME

logger = logging.getLogger(__name__)


class Database:
    """Async MongoDB database operations"""
    
    def __init__(self):
        self.client: AsyncIOMotorClient = None
        self.db: AsyncIOMotorDatabase = None
    
    async def connect(self):
        """Connect to MongoDB"""
        try:
            self.client = AsyncIOMotorClient(MONGODB_URI)
            self.db = self.client[DATABASE_NAME]
            
            # Verify connection
            await self.db.command('ping')
            logger.info("✅ Connected to MongoDB")
            
            # Create indexes
            await self._create_indexes()
        except Exception as e:
            logger.error(f"❌ Failed to connect to MongoDB: {str(e)}")
            raise
    
    async def disconnect(self):
        """Disconnect from MongoDB"""
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")
    
    async def _create_indexes(self):
        """Create necessary database indexes"""
        try:
            # Users collection indexes
            await self.db.users.create_index('user_id', unique=True)
            
            # Applications collection indexes
            await self.db.applications.create_index('user_id')
            await self.db.applications.create_index([('user_id', 1), ('name', 1)])
            
            # Codespaces collection indexes
            await self.db.codespaces.create_index('user_id')
            await self.db.codespaces.create_index('app_id')
            
            # Billing logs indexes
            await self.db.billing_logs.create_index('user_id')
            await self.db.billing_logs.create_index('timestamp')
            
            logger.info("✅ Database indexes created")
        except Exception as e:
            logger.error(f"Error creating indexes: {str(e)}")
    
    # User operations
    async def create_or_get_user(self, user_id: int, username: str, first_name: str = "") -> dict:
        """Create or get user"""
        try:
            user = await self.db.users.find_one({'user_id': user_id})
            
            if user:
                return user
            
            # Create new user
            new_user = {
                'user_id': user_id,
                'username': username,
                'first_name': first_name,
                'github_tokens': [],
                'applications': [],
                'billing_alerts': True,
                'usage_limits': {
                    'monthly_hours': 120,
                    'monthly_storage_gb': 15
                },
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            }
            
            result = await self.db.users.insert_one(new_user)
            new_user['_id'] = result.inserted_id
            return new_user
        
        except Exception as e:
            logger.error(f"Error creating/getting user: {str(e)}")
            return {}
    
    async def get_user(self, user_id: int) -> dict:
        """Get user by ID"""
        try:
            user = await self.db.users.find_one({'user_id': user_id})
            return user or {}
        except Exception as e:
            logger.error(f"Error getting user: {str(e)}")
            return {}
    
    async def add_github_token(self, user_id: int, token: str) -> bool:
        """Add GitHub API token to user"""
        try:
            token_id = str(uuid.uuid4())
            token_info = {
                '_id': token_id,
                'token': token,
                'is_active': True,
                'added_at': datetime.utcnow(),
                'last_used': None
            }
            
            # Deactivate all other tokens
            await self.db.users.update_one(
                {'user_id': user_id},
                {'$set': {'github_tokens.$[].is_active': False}}
            )
            
            # Add new token
            result = await self.db.users.update_one(
                {'user_id': user_id},
                {'$push': {'github_tokens': token_info}}
            )
            
            return result.modified_count > 0
        
        except Exception as e:
            logger.error(f"Error adding GitHub token: {str(e)}")
            return False
    
    async def switch_token(self, user_id: int, token_id: str) -> bool:
        """Switch active GitHub token"""
        try:
            # Deactivate all tokens
            await self.db.users.update_one(
                {'user_id': user_id},
                {'$set': {'github_tokens.$[].is_active': False}}
            )
            
            # Activate selected token
            result = await self.db.users.update_one(
                {'user_id': user_id, 'github_tokens._id': token_id},
                {'$set': {'github_tokens.$.is_active': True}}
            )
            
            return result.modified_count > 0
        
        except Exception as e:
            logger.error(f"Error switching token: {str(e)}")
            return False
    
    async def delete_token(self, user_id: int, token_id: str) -> bool:
        """Delete GitHub token"""
        try:
            result = await self.db.users.update_one(
                {'user_id': user_id},
                {'$pull': {'github_tokens': {'_id': token_id}}}
            )
            
            return result.modified_count > 0
        
        except Exception as e:
            logger.error(f"Error deleting token: {str(e)}")
            return False
    
    # Application operations
    async def create_application(self, user_id: int, app_name: str) -> str:
        """Create new application"""
        try:
            app_id = str(uuid.uuid4())
            new_app = {
                '_id': app_id,
                'user_id': user_id,
                'name': app_name,
                'repo_url': '',
                'forked_repo': '',
                'env_vars': {},
                'build_command': '',
                'start_command': '',
                'docker_enabled': False,
                'status': 'inactive',
                'codespace_id': '',
                'codespace_name': '',
                'machine_type': 'medium',
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow(),
                'last_started': None,
                'last_stopped': None
            }
            
            await self.db.applications.insert_one(new_app)
            
            # Add to user's applications list
            await self.db.users.update_one(
                {'user_id': user_id},
                {'$push': {'applications': app_id}}
            )
            
            return app_id
        
        except Exception as e:
            logger.error(f"Error creating application: {str(e)}")
            return ""
    
    async def get_application(self, app_id: str) -> dict:
        """Get application by ID"""
        try:
            app = await self.db.applications.find_one({'_id': app_id})
            return app or {}
        except Exception as e:
            logger.error(f"Error getting application: {str(e)}")
            return {}
    
    async def get_user_applications(self, user_id: int) -> list:
        """Get all applications for a user"""
        try:
            apps = await self.db.applications.find({'user_id': user_id}).to_list(None)
            return apps or []
        except Exception as e:
            logger.error(f"Error getting user applications: {str(e)}")
            return []
    
    async def update_application(self, app_id: str, update_data: dict) -> bool:
        """Update application"""
        try:
            update_data['updated_at'] = datetime.utcnow()
            result = await self.db.applications.update_one(
                {'_id': app_id},
                {'$set': update_data}
            )
            
            return result.modified_count > 0
        
        except Exception as e:
            logger.error(f"Error updating application: {str(e)}")
            return False
    
    async def delete_application(self, user_id: int, app_id: str) -> bool:
        """Delete application"""
        try:
            await self.db.applications.delete_one({'_id': app_id})
            
            # Remove from user's applications list
            await self.db.users.update_one(
                {'user_id': user_id},
                {'$pull': {'applications': app_id}}
            )
            
            return True
        
        except Exception as e:
            logger.error(f"Error deleting application: {str(e)}")
            return False
    
    # Codespace operations
    async def create_codespace_log(self, user_id: int, app_id: str, codespace_id: str, codespace_data: dict):
        """Log new Codespace creation"""
        try:
            new_codespace = {
                '_id': codespace_id,
                'user_id': user_id,
                'app_id': app_id,
                'codespace_name': codespace_data.get('name'),
                'repo_name': codespace_data.get('repository', {}).get('name'),
                'branch': codespace_data.get('branch', 'main'),
                'state': codespace_data.get('state', 'In Progress'),
                'web_url': codespace_data.get('web_url'),
                'machine_type': codespace_data.get('machine', {}).get('name', 'standard'),
                'created_at': datetime.utcnow(),
                'started_at': datetime.utcnow(),
                'last_used_at': datetime.utcnow(),
                'retention_period_minutes': 30
            }
            
            await self.db.codespaces.insert_one(new_codespace)
        
        except Exception as e:
            logger.error(f"Error creating codespace log: {str(e)}")
    
    async def get_user_codespaces(self, user_id: int) -> list:
        """Get all Codespaces for a user"""
        try:
            codespaces = await self.db.codespaces.find({'user_id': user_id}).to_list(None)
            return codespaces or []
        except Exception as e:
            logger.error(f"Error getting user codespaces: {str(e)}")
            return []
    
    async def log_billing(self, user_id: int, app_id: str, codespace_id: str, 
                         action: str, machine_type: str, duration: int = 0, cost: float = 0.0):
        """Log billing event"""
        try:
            billing_log = {
                'user_id': user_id,
                'app_id': app_id,
                'codespace_id': codespace_id,
                'action': action,
                'machine_type': machine_type,
                'duration_minutes': duration,
                'cost': cost,
                'timestamp': datetime.utcnow()
            }
            
            await self.db.billing_logs.insert_one(billing_log)
        
        except Exception as e:
            logger.error(f"Error logging billing: {str(e)}")


# Global database instance
db = Database()
