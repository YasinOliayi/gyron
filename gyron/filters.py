import re
from typing import Union, Callable
from .models import Update
from .state import StateManager
import asyncio
class filters:
    __slots__ = ()   

    @staticmethod
    def text(pattern = None) -> Callable:
        
      
        if pattern is None:
         
            return lambda message: message.text is not None

        elif isinstance(pattern, str):
            compiled = re.compile(pattern)
        else:
            compiled = pattern


        return lambda message: bool(message.text and compiled.search(message.text))
    
    @staticmethod
    def caption(pattern = None):

        if pattern is None:

            return lambda message: message.caption is not None
        
        elif isinstance(pattern, str):

            compiled = re.compile(pattern)
        
        else:
            compiled = pattern

        return lambda message: bool(message.caption and compiled.search(message.caption))
        
    
    @staticmethod
    def private() -> Callable :


        return lambda message: message.chat.type == 'private'
    
    @staticmethod
    def group():


        return lambda message: message.chat.type == 'group'
    
    @staticmethod
    def channel():

        return lambda message: message.chat.type == 'channel'



    @staticmethod
    def new_member():

        def _filter(update:Update):

            return bool(update.new_chat_member)
        return _filter
    
    @staticmethod
    def left_member():

        return lambda message: message.left_chat_member.id is not None


    @staticmethod
    def is_referral():

        def _filter(message):
            
            if message.text is None:
                return False



            result = message.text.split(maxsplit = 1)

            if len(result) == 2 and result[0] == "/start" and result[1].isdigit():
                return True
            return False
        return _filter
    
    
    @staticmethod
    def is_joined(*chat_ids: Union[str, int]):

        async def _filter(message: Update):

            bot = message._bot

            responses = await asyncio.gather(
            *(
                bot.get_chat_member(chat_id, user_id=message.author.id)
                for chat_id in chat_ids
            )
        )

            return all(
            response.status in ('member', 'creator', 'administrator')
            for response in responses
        )

        return _filter
                    



    @staticmethod
    def not_is_joined(*chat_ids: Union[str, int]):

        async def _filter(message: Update):

            bot = message._bot

            responses = await asyncio.gather(
            *(
                bot.get_chat_member(chat_id, user_id=message.author.id)
                for chat_id in chat_ids
            )
        )

            return all(
            response.status not in ('member', 'creator', 'administrator')
            for response in responses
        )

        return _filter
    
    
    @staticmethod
    def pre_checkout_query():

        def _filter(message:Update):

            if message.pre_checkout_query.id:

                return True
            return False
        return _filter
    
    
    @staticmethod
    def at_state(manager : StateManager, state : str = None):


        async def _filter(message: Update):


            if message.author.id :

                current_state = await manager.get_state_for(message)

                if state is None:
                    return current_state is not None
                
                return current_state == state
            
        return _filter
    
    
    @staticmethod
    def callback_query(button_data : str = None):
    


        def _filter(message: Update):


            if button_data is None:

                return message.callback_query.data is not None
            
            return message.callback_query.data == button_data
        
        return _filter
    
    
    @staticmethod
    def contact(phone_number : str = None):


        def _filter(message:Update):

            if phone_number is None:

                return message.contact.phone_number is not None
            return message.contact.phone_number == phone_number
        
        return _filter
    
    @staticmethod
    def location():


        def _filter(message:Update):

            return message.location.latitude is not None
        return _filter
    

    @staticmethod
    def forward():


        def _filter(message:Update):

            return message.forward_date is not None
        return _filter
    
    @staticmethod
    def document():


        def _filter(message:Update):

            return message.document.id is not None
        return _filter
    
    
    
    @staticmethod
    def photo():

        def _filter(message:Update):


            return message.photo
        return _filter
        
    @staticmethod
    def reply():


        def _filter(message:Update):

            return message.reply.message_id is not None
        return _filter
    

    @staticmethod
    def voice():


        def _filter(message:Update):

            return message.voice.id is not None
        return _filter
    
    @staticmethod
    def animation():


        def _filter(message:Update):

            return message.animation.id is not None
        return _filter
    
    @staticmethod
    def video():

        def _filter(message:Update):

            return message.video.id is not None
        return _filter
    
    @staticmethod
    def sticker():

        def _filter(message:Update):

            return message.sticker.id is not None
            
        return _filter
        
    @staticmethod
    def successful_payment():

        def _filter(message:Update):

            return message.successful_payment.currency is not None
        return _filter
    
    @staticmethod
    def invoice():

        def _filter(message:Update):

            return message.invoice.total_amount is not None
        return _filter
    
    @staticmethod
    def entity():

        def _filter(message:Update):

            return message.entities

            
        return _filter

    
    @staticmethod
    def equals(text : str):

        return lambda message: message.text == text


    @staticmethod
    def is_admin():

        async def _filter(update:Update):
            
            if update.chat.type == "private":
                return False

            bot = update._bot
            user_id = update.author.id
            
            if user_id is None:
                user_id = update.callback_query.author.id
                
            if user_id is None:
                return False
            
            response = await bot.get_chat_member(update.chat.id, user_id)

            return response.status == 'administrator'
        return _filter

    @staticmethod
    def is_member():
    
        async def _filter(update:Update):
            
            if update.chat.type == "private":
                return False
    
            bot = update._bot
            user_id = update.author.id
            
            if user_id is None:
                user_id = update.callback_query.author.id
            
            if user_id is None:
                return False
                   
            response = await bot.get_chat_member(update.chat.id, user_id)
    
            return response.status == 'member'
        return _filter


    @staticmethod
    def is_creator():
    
        async def _filter(update:Update):
            
            if update.chat.type == "private":
                return False
    
            bot = update._bot
            user_id = update.author.id
            
            if user_id is None:
                user_id = update.callback_query.author.id
            
            if user_id is None:
                return False
                
                
            response = await bot.get_chat_member(update.chat.id, user_id)
    
            return response.status == 'creator'
        return _filter


    @staticmethod
    def is_restricted():
        
        async def _filter(update:Update):
            
            if update.chat.type == "private":
                return False
        
            bot = update._bot
            user_id = update.author.id
            
            if user_id is None:
                user_id = update.callback_query.author.id
                
            if user_id is None:
                return False
                
                
            response = await bot.get_chat_member(update.chat.id, user_id)
        
            return response.status == 'restricted'
        return _filter
        
    
    @staticmethod
    def user_id(id : Union[str, int]):


        def _filter(update :Update):
            
            user_id = update.author.id or update.callback_query.author.id
            
            if user_id is None:
                return False
            
            return id == user_id

            
        
        return _filter
    
    
    @staticmethod
    def chat_id(id : Union[str, int]):


        def _filter(update : Update):

            chat_id = update.chat.id
            
            if chat_id is None:
                return False
            
            return id == chat_id
        
        return _filter
    
    
    @staticmethod
    def command(command: str = None):

        def _filter(update):
            text = update.text
            
            if update.text is None:
                return False
                

            if command is None:
                return text.startswith("/")

            return text == f"/{command}"

        return _filter
        





