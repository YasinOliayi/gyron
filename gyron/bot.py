import asyncio
import sys
from typing import Union, List, Any
import httpx
import json
from contextvars import ContextVar
import aiofiles
from collections import defaultdict
from .models import (Keypad, InlineKeypad, Update, LabeledPrice, ChatFullInfo, File, InputMediaPhoto,
                      MessageResponse, GetMeResponse, ChatAdministratorsResponse, ChatMember, EditedMessage,
                        WebhookInfo, SendMediaResult, SendMediaGroupResult, ApiResponse)

from .enums import ActionsEnum


sys.stdout.reconfigure(encoding='utf-8')


class BotClient:
    __slots__ = ('token', 'base_url', 'offset', 'handler',
                  'session', 'use_webhook', '_bot_username',
                    '_current_message', '_queues', '_workers',
                    '_worker_locks', 'download_base_url' ,"_middlewares")

    def __init__(self, token: str, use_webhook : bool = False):
        self.token = token
        self.base_url = f'https://tapi.bale.ai/bot{token}'
        self.offset = -1
        self.handler = []
        self.session = httpx.AsyncClient()
        self.use_webhook = use_webhook
        self._bot_username = None
        self._current_message = ContextVar('current_message', default= None)
        self._queues = {}
        self._workers = {}
        self._worker_locks = defaultdict(asyncio.Lock)
        self.download_base_url = f'https://tapi.bale.ai/file/bot{token}/'
        self._middlewares = []
      
  
        


    def on_update(self, *filter_func):
        def decorator(user_function):
       

            self.handler.append({'func': user_function, 'filter': filter_func})
            
        return decorator
  
        
           
    def middleware(self):
        
        def decorator(user_function):
            
            self._middlewares.append(user_function)
            
        
        return decorator
        
        
        
    async def get_updates(self, offset: int = None, limit: int = None, timeout: int = None, request_timeout : int = None
) -> dict[str, Any] :
        payload = {}

        if offset is not None:
            payload["offset"] = offset

        if limit is not None:
            payload["limit"] = limit

        if timeout is not None:
            payload["timeout"] = timeout

        response = await self.session.post(
        f"{self.base_url}/getUpdates",
        json=payload, timeout = request_timeout
    )
        return response.json()
    


    async def send_message(self, chat_id: Union[str, int], text: str, markup : Union[InlineKeypad, Keypad]=None, reply_to_message_id : int = None) -> MessageResponse :
    
        data = {
            'chat_id': chat_id,
            'text': text  
        }
        if markup:
            data['reply_markup'] = markup
        
        if reply_to_message_id:
            data["reply_to_message_id"] = reply_to_message_id
            
        response = await self.session.post(f'{self.base_url}/sendMessage', data=data)

        return MessageResponse(response.json())
  
      
    
    async def get_me(self) -> GetMeResponse:

        response = await self.session.post(f'{self.base_url}/getMe')
        
        return GetMeResponse(response.json())




    async def set_webhook(self, url: str) -> ApiResponse:
        
        data = {'url': url}
        
        response = await self.session.post(f'{self.base_url}/setWebhook', data=data)
        
        return ApiResponse(response.json())




    async def delete_webhook(self) -> ApiResponse:
        
        response = await self.session.post(f'{self.base_url}/deleteWebhook')
        
        return ApiResponse(response.json())



    async def get_webhook_info(self) -> WebhookInfo:

        response = await self.session.post(f'{self.base_url}/getWebhookinfo')
        
        return WebhookInfo(response.json())


    async def forward_message(self, from_chat_id: Union[str, int], chat_id: Union[str, int], message_id: int) -> MessageResponse:
        data = {
            'chat_id': chat_id,
            'from_chat_id': from_chat_id,
            'message_id': message_id
        }
        response = await self.session.post(f'{self.base_url}/forwardMessage', data=data)
        return MessageResponse(response.json())

    async def copy_message(self, from_chat_id: Union[str, int], chat_id: Union[str, int], message_id: int) -> MessageResponse:
        data = {
            'chat_id': chat_id,
            'from_chat_id': from_chat_id,
            'message_id': message_id
        }
        response = await self.session.post(f'{self.base_url}/copyMessage', data=data)
        return MessageResponse(response.json())



    async def reply(self, text: str, markup : Union[Keypad, InlineKeypad]=None) -> Union[MessageResponse, None]:

        message = self._current_message.get()

        if message is None:
            return None
    
        data = {
            'chat_id': message['chat_id'],
            'text': text,
            'reply_to_message_id': message['message_id']
        }
        if markup:
            data['reply_markup'] = markup
            
        response = await self.session.post(f'{self.base_url}/sendMessage', data=data)


        return MessageResponse(response.json())



    async def send_photo(self, chat_id: Union[str, int], file: str, from_chat_id: Union[str, int] = None,
                         caption: str = None, reply_to_message_id: int = None, markup : Union[InlineKeypad, Keypad]=None, is_local_file: bool = False) -> SendMediaResult:
        data = {'chat_id': chat_id, 'caption': caption}
        if from_chat_id:
            data['from_chat_id'] = from_chat_id
        if reply_to_message_id:
            data['reply_to_message_id'] = reply_to_message_id
        if markup:
            data['reply_markup'] = markup

        if not is_local_file:
            data['photo'] = file
            response = await self.session.post(f'{self.base_url}/sendPhoto', data=data)

            data_json = response.json()
            return SendMediaResult(data_json)
            
        
        else:
            try:
                with open(file, 'rb') as f:
                    files = {'photo': f}
                    response = await self.session.post(f'{self.base_url}/sendPhoto', data=data, files=files)

                    data_json = response.json()

                    return SendMediaResult(data_json)
                  
                    
            except FileNotFoundError:
                print(f'not found file {file}')


    async def send_audio(self, chat_id: Union[str, int], file: str, caption: str = None,
                         reply_to_message_id: int = None, markup : Union[InlineKeypad, Keypad]=None, is_local_file: bool = False) -> SendMediaResult:
        data = {'chat_id': chat_id, 'caption': caption}
        if reply_to_message_id:
            data['reply_to_message_id'] = reply_to_message_id
        if markup:
            data['reply_markup'] = markup

        if not is_local_file:
            data['audio'] = file
            response = await self.session.post(f'{self.base_url}/sendAudio', data=data)
            return SendMediaResult(response.json())
        else:
            try:
                with open(file, 'rb') as f:
                    files = {'audio': f}
                    response = await self.session.post(f'{self.base_url}/sendAudio', data=data, files=files)
                    return SendMediaResult(response.json())
            except FileNotFoundError:
                print(f'not found file {file}')


    async def send_document(self, chat_id: Union[str, int], file: str, caption: str = None,
                            reply_to_message_id: int = None, markup : Union[InlineKeypad, Keypad]=None, is_local_file: bool = False) -> SendMediaResult:
        
        data = {'chat_id': chat_id, 'caption': caption}
        if reply_to_message_id:
            data['reply_to_message_id'] = reply_to_message_id
        if markup:
            data['reply_markup'] = markup

        if not is_local_file:

            data['document'] = file

            response = await self.session.post(f'{self.base_url}/sendDocument', data=data)

            return SendMediaResult(response.json())
        
        else:
            try:

                with open(file, 'rb') as f:
                    files = {'document': f}

                    response = await self.session.post(f'{self.base_url}/sendDocument', data=data, files=files)

                    return SendMediaResult(response.json())
                
            except FileNotFoundError:
                print(f'not found file {file}')


    async def send_video(self, chat_id: Union[str, int], file: str, caption: str = None,
                         reply_to_message_id: int = None, markup : Union[InlineKeypad, Keypad]=None, is_local_file: bool = False) -> SendMediaResult:
        data = {'chat_id': chat_id, 'caption': caption}
        if reply_to_message_id:
            data['reply_to_message_id'] = reply_to_message_id
        if markup:
            data['reply_markup'] = markup

        if not is_local_file:

            data['video'] = file

            response = await self.session.post(f'{self.base_url}/sendVideo', data=data)

            return SendMediaResult(response.json())
        
        else:
            try:

                with open(file, 'rb') as f:

                    files = {'video': f}

                    response = await self.session.post(f'{self.base_url}/sendVideo', data=data, files=files)

                    return SendMediaResult(response.json())
                
            except FileNotFoundError:

                print(f'not found file {file}')


    async def send_animation(self, chat_id: Union[str, int], file: str, caption: str = None,
                             reply_to_message_id: int = None, markup : Union[InlineKeypad, Keypad]=None, is_local_file: bool = False) -> SendMediaResult:
        data = {'chat_id': chat_id, 'caption': caption}
        if reply_to_message_id:
            data['reply_to_message_id'] = reply_to_message_id
        if markup:
            data['reply_markup'] = markup

        if not is_local_file:
            data['animation'] = file
            response = await self.session.post(f'{self.base_url}/sendAnimation', data=data)
            return SendMediaResult(response.json())
        else:
            try:
                with open(file, 'rb') as f:
                    files = {'animation': f}
                    response = await self.session.post(f'{self.base_url}/sendAnimation', data=data, files=files)
                    return SendMediaResult(response.json())
            except FileNotFoundError:
                print(f'not found file {file}')



    async def send_voice(self, chat_id: Union[str, int], file: str, caption: str = None,
                         reply_to_message_id: int = None, markup : Union[InlineKeypad, Keypad]=None, is_local_file: bool = False) -> SendMediaResult:
        
        data = {'chat_id': chat_id}

        if reply_to_message_id:
            data['reply_to_message_id'] = reply_to_message_id

        if markup:
            data['reply_markup'] = markup

        if caption:

            data['caption'] = caption

        if not is_local_file:

            data['voice'] = file

        
            response = await self.session.post(f'{self.base_url}/sendVoice', data=data)

            return SendMediaResult(response.json())
        
        else:

            try:

                with open(file, 'rb') as f:
                
                    files = {
                        "voice": f
                    }

                    response = await self.session.post(f'{self.base_url}/sendVoice', data=data, files=files)
                  
                    return SendMediaResult(response.json())
                
            except FileNotFoundError:

                print(f'not found file {file}')
           


    async def send_media_group(self, chat_id : Union[str, int], media : List[InputMediaPhoto], reply_to_message_id : int = None) -> SendMediaGroupResult:

        result = []
        files = {}
        opened_files = []

        for i in media:
            d = i.to_dict()

            if i.is_local_file:
                files_name = i.file_name or "file"
                
                

                f = open(i.media, "rb")
                opened_files.append(f)
                
                files[files_name] = (
                    files_name,
                    f
                )

                
                

            result.append(d)

        data = {
        "chat_id": str(chat_id),
        "media": json.dumps(result)}

        if reply_to_message_id:
             data["reply_to_message_id"] = str(reply_to_message_id)
             
             
        try:
                
            response = await self.session.post(
            f"{self.base_url}/sendMediaGroup",
                data=data,
                files=files if files else None
        )
        
    
            return SendMediaGroupResult(response.json())
        
        finally:
            
            for f in opened_files:
                f.close()
            
        


    async def send_location(self, chat_id: Union[str, int], latitude: float, longitude: float,
                            horizontal_accuracy: float = None, reply_to_message_id: int = None, markup : Union[InlineKeypad, Keypad]=None) -> ApiResponse:
        data = {
            'chat_id': chat_id,
            'latitude': latitude,
            'longitude': longitude,
        }
        if horizontal_accuracy:
            data['horizontal_accuracy'] = horizontal_accuracy
        if reply_to_message_id:
            data['reply_to_message_id'] = reply_to_message_id
        if markup:
            data['reply_markup'] = markup
        response = await self.session.post(f'{self.base_url}/sendLocation', data=data)

        return ApiResponse(response.json())


    async def send_contact(self, chat_id : Union[str, int], phone_number : str, first_name: str, last_name : str=None,
                           reply_to_message_id: int =None, markup : Union[InlineKeypad, Keypad]=None) -> ApiResponse:
        data = {
            'chat_id': chat_id,
            'phone_number': phone_number,
            'first_name': first_name
        }
        if last_name:
            data['last_name'] = last_name
        if reply_to_message_id:
            data['reply_to_message_id'] = reply_to_message_id
        if markup:
            data['reply_markup'] = markup
        response = await self.session.post(f'{self.base_url}/sendContact', data=data)

        return ApiResponse(response.json())


    async def send_action(self, chat_id: Union[str, int], action : Union[str, ActionsEnum]) -> ApiResponse:
        
        data = {'chat_id': chat_id}
        if isinstance(action, str):
            data['action'] = action
        else:
            data['action'] = action.value
            
        response = await self.session.post(f'{self.base_url}/sendChatAction', data=data)
        
        return ApiResponse(response.json())



    async def get_file(self, file_id: str) -> File:
        data = {'file_id': file_id}
        
        response = await self.session.post(f'{self.base_url}/getFile', data=data)
        
        return File(response.json())


    async def answer_callback_query(self, callback_id : str, text : str = None, show_alert: bool = False) -> ApiResponse:
        
        data = {'callback_query_id': callback_id}
        
        if text:
            data['text'] = text
        if show_alert:
            data['show_alert'] = show_alert
            
        response = await self.session.post(f'{self.base_url}/AnswerCallbackQuery', data=data)
        
        return ApiResponse(response.json())


    async def ask_review(self, user_id : int, delay : int) -> ApiResponse:
        
        if not 0 <= delay <= 10:
            raise ValueError(
    "Invalid value in ask_review(): delay must be between 0 and 10 seconds."
)
        
        data = {'user_id': user_id, 'delay_seconds': delay}
        
        response = await self.session.post(f'{self.base_url}/askReview', data=data)
        
        return ApiResponse(response.json())



    async def ban_member(self, chat_id : Union[str, int], user_id : int) -> ApiResponse:
        
        data = {'chat_id': chat_id, 'user_id': user_id}
        
        response = await self.session.post(f'{self.base_url}/banChatMember', data=data)
        
        return ApiResponse(response.json())


    async def unban_member(self, chat_id : Union[str, int], user_id : int, only_if_banned : bool = False) -> ApiResponse:
        
        data = {'chat_id': chat_id, 'user_id': user_id}
        
        if only_if_banned:
            data['only_if_banned'] = only_if_banned
            
        response = await self.session.post(f'{self.base_url}/unbanChatMember', data=data)
        
        return ApiResponse(response.json())



    async def promote_member(self, chat_id: Union[str, int], user_id: int,
                                  can_change_info: bool = False, can_post_messages: bool = False,
                                  can_edit_messages: bool = False, can_delete_messages: bool = False,
                                  can_manage_video_chats: bool = False, can_invite_users: bool = False,
                                  can_restrict_members: bool = False) -> ApiResponse:
                                      
        data = {'chat_id': chat_id, 'user_id': user_id}
        
        if can_change_info:
            data['can_change_info'] = can_change_info
        if can_post_messages:
            data['can_post_messages'] = can_post_messages
        if can_edit_messages:
            data['can_edit_messages'] = can_edit_messages
        if can_delete_messages:
            data['can_delete_messages'] = can_delete_messages
        if can_manage_video_chats:
            data['can_manage_video_chats'] = can_manage_video_chats
        if can_invite_users:
            data['can_invite_users'] = can_invite_users
        if can_restrict_members:
            data['can_restrict_members'] = can_restrict_members
            
        response = await self.session.post(f'{self.base_url}/promoteChatMember', data=data)
        
        return ApiResponse(response.json())
  
      
    async def set_chat_photo(self, chat_id : Union[str, int], file : str, is_local_file : bool = False) -> ApiResponse:


        data = {
            'chat_id' : chat_id
        }

        if is_local_file:
            try:

                with open(file, 'rb') as f:

                    photo_file = {'photo' : f}

                    response = await self.session.post(f'{self.base_url}/setChatPhoto', data= data, files= photo_file)
                    
                    return ApiResponse(response.json())

            except FileNotFoundError:
                print(f'not found file : {file}')
        
        else:

            data['photo'] = file

            response = await self.session.post(f'{self.base_url}/setChatPhoto', data= data)

            return ApiResponse(response.json())
    
            
    
    async def leave_chat(self, chat_id : Union[str, int]) -> ApiResponse:
        
        data = {
            'chat_id' : chat_id
        } 
        response = await self.session.post(f'{self.base_url}/leaveChat', data= data)
        
        return ApiResponse(response.json())
    
    

    async def get_chat(self, chat_id : Union[str, int]) -> ChatFullInfo:
        data = {
            'chat_id' : chat_id
        } 
        response = await self.session.post(f'{self.base_url}/getChat', data= data)
      
        return ChatFullInfo(response.json())
    

    async def get_chat_administrators(self, chat_id : Union[str, int]) -> ChatAdministratorsResponse:
        data = {
            'chat_id' : chat_id
        } 
        response = await self.session.post(f'{self.base_url}/getChatAdministrators', data= data)
        return ChatAdministratorsResponse(response.json())
    

    async def get_chat_member_count(self, chat_id : Union[str, int]) -> Union[int, None]:
        data = {
            'chat_id' : chat_id
        } 
        response = await self.session.post(f'{self.base_url}/getChatMemberCount', data= data)
        
        data = response.json()
        
        if data.get("ok"):
            return data.get("result")
        return None
    
    
    async def get_chat_member(self, chat_id : Union[str, int], user_id : int) -> ChatMember:
        data = {
            'chat_id' : chat_id,
            'user_id' : user_id
        } 
        response = await self.session.post(f'{self.base_url}/getChatMember', data= data)
        return ChatMember(response.json())
    

    async def pin_message(self, chat_id : Union[str, int], message_id : int) -> ApiResponse:
        data = {
            'chat_id' : chat_id,
            'message_id': message_id
        } 
        response = await self.session.post(f'{self.base_url}/pinChatMessage', data= data)
        
        return ApiResponse(response.json())
        
        
    
    async def unpin_message(self, chat_id : Union[str, int], message_id : int) -> ApiResponse:
        data = {
            'chat_id' : chat_id,
            'message_id': message_id
        } 
        response = await self.session.post(f'{self.base_url}/unPinChatMessage', data= data)
        
        return ApiResponse(response.json())
    

    async def unpin_all_message(self, chat_id : Union[str, int]) -> ApiResponse:
        data = {
            'chat_id' : chat_id
        } 
        response = await self.session.post(f'{self.base_url}/unpinAllChatMessage', data= data)
        
        return ApiResponse(response.json())
    

    async def set_chat_description(self, chat_id : Union[str, int], description : str) -> ApiResponse:
        
        data = {
            'chat_id' : chat_id,
            'description': description
        } 
        response = await self.session.post(f'{self.base_url}/setChatDescription', data= data)
        
        return ApiResponse(response.json())
    

    async def delete_chat_photo(self, chat_id : Union[str, int]) -> ApiResponse:
        
        data = {
            'chat_id' : chat_id
        } 
        response = await self.session.post(f'{self.base_url}/deleteChatPhoto', data= data)
        
        return ApiResponse(response.json())
    

    async def create_invite_link(self, chat_id : Union[str, int]) -> Union[str, None]:
        
        data = {
            'chat_id' : chat_id
        } 
        response = await self.session.post(f'{self.base_url}/createChatInviteLink', data= data)
        
        data = response.json()
        
        return data.get("result", {}).get("invite_link") if data.get("ok") else None
    
    

    async def revoke_invite_link(self, chat_id : Union[str, int], invite_link : str) -> Union[str, None]:
        data = {
            'chat_id' : chat_id,
            'invite_link' : invite_link
        } 
        response = await self.session.post(f'{self.base_url}/revokeChatInviteLink', data= data)
        
        data = response.json()
        
        return data.get("result", {}).get("invite_link") if data.get("ok") else None
    

        
    async def export_invite_link(self, chat_id : Union[str, int]) -> Union[str, None] :
        data = {
            'chat_id' : chat_id
        } 
        response = await self.session.post(f'{self.base_url}/exportChatInviteLink', data= data)
        
        data = response.json()
        
        return data.get("result") if data.get("ok") else None
    
    
    
    
    async def edit_message(self, chat_id: Union[str, int],message_id : int, text: str, markup : Union[InlineKeypad, Keypad] = None) -> EditedMessage:
        
        data = {
            'chat_id': chat_id,
            'message_id' : message_id,
            'text' : text
            }
            
        if markup:
            data['reply_markup'] = markup
            
        response = await self.session.post(f'{self.base_url}/editMessageText', data=data)
        
        return EditedMessage(response.json())
    
    
    
    
    async def edit_caption(self, chat_id: Union[str, int],message_id : int, caption: str = None, markup : Union[InlineKeypad, Keypad] = None) -> EditedMessage:
        data = {
            'chat_id': chat_id,
            'message_id' : message_id 
            }
        if markup:
            data['reply_markup'] = markup
        if caption:
            data['caption'] = caption
        response = await self.session.post(f'{self.base_url}/editMessageCaption', data=data)
        return EditedMessage(response.json())
    
  
  
    async def edit_markup(self, chat_id: Union[str, int], message_id : int, markup : Union[InlineKeypad, Keypad]) -> EditedMessage:

        data = {
            'chat_id' : chat_id,
            'message_id' : message_id,
            'reply_markup' : markup
        }

        response = await self.session.post(f'{self.base_url}/editMessageReplyMarkup', data=data)
        return EditedMessage(response.json())



    async def delete_message(self, chat_id: Union[str, int], message_id : int) -> ApiResponse:

        data = {
            'chat_id' : chat_id,
            'message_id' : message_id
        }

        response = await self.session.post(f'{self.base_url}/deleteMessage', data=data)
        
        return ApiResponse(response.json())
    
    
    
    async def send_invoice(self, chat_id: Union[str, int], title: str,
                            description: str, payload: str, provider_token : str,
                            prices : List[LabeledPrice], photo_url : str = None, reply_to_message_id : int = None) -> MessageResponse:
        
        data = {
            'chat_id' : chat_id,
            'title' : title,
            'description' : description,
            'payload' : payload,
            'provider_token' : provider_token    
        }

        if not prices:
            raise ValueError('prices list cannot be empty')

        if isinstance(prices, list):
            data['prices'] = json.dumps([i.to_dict() for i in prices])
        else:
            raise TypeError ('prices must be a list')
        
        if photo_url:
            data['photo_url'] = photo_url
        if reply_to_message_id:
            data['reply_to_message_id'] = reply_to_message_id

        response = await self.session.post(f'{self.base_url}/sendInvoice', data=data)

        return MessageResponse(response.json())
    
    
    

    async def create_invoice_link(self, title: str,
                            description: str, payload: str, provider_token : str, prices : List[LabeledPrice]) -> Union[str, None]:
        
        data = {
            
            'title' : title,
            'description' : description,
            'payload' : payload,
            'provider_token' : provider_token            
        }

        if not prices:
            raise ValueError('prices list cannot be empty')
        
        if isinstance(prices, list):
            data['prices'] = json.dumps([i.to_dict() for i in prices])
        
        else:
            raise TypeError ('prices must be a list')
        
        
        response = await self.session.post(f'{self.base_url}/createInvoiceLink', data=data)

        data = response.json()

        if data.get('ok'):

            return data.get('result')
        return None
    
    
    

    async def answer_pre_checkout_query(self, pre_checkout_query_id : str, ok : bool, error_message: str = None) -> ApiResponse:


        data = {'pre_checkout_query_id' : pre_checkout_query_id}

        
        data['ok'] = ok
        
        if not ok:

            data['error_message'] = error_message

        response = await self.session.post(f'{self.base_url}/answerPreCheckoutQuery', data=data)

        return ApiResponse(response.json())
    
    
    
    async def inquire_transaction(self, transaction_id : str) -> dict:

        data = {
            'transaction_id' : transaction_id
        }


        response = await self.session.post(f'{self.base_url}/inquireTransaction', data=data)

        return response.json()
    
    
    
    async def create_referral_link(self, payload : Union[str, int]) -> str:

        
        return f"https://ble.ir/{self._bot_username}?start={payload}"
    
    
    
    
    async def extract_referral_payload(self, text : str) -> Union[int, None] :

        result = text.split(maxsplit=1)

        if len(result) == 2 and result[0] == '/start' and result[1].isdigit():
            return int(result[1])
 
        return None
    
    
    async def create_new_sticker_set(self, user_id : int, name: str, title : str, sticker) -> dict:


        data = {
            'user_id' : user_id,
            'name' : name,
            'title' : title,
            'sticker' : sticker
            
        } 


        response = await self.session.post(f'{self.base_url}/createNewStickerSet', data= data)
        return response.json()
    
    
    
    async def add_sticker_to_set(self, user_id : int, name : str, sticker) -> dict:

        data = {
            'user_id' : user_id,
            'name' : name,
            'sticker' : sticker
        } 

        response = await self.session.post(f'{self.base_url}/addStickerToSet', data= data)
        return response.json()



    async def upload_sticker_file(self, user_id : int, sticker) -> dict:
    
            data = {
                'user_id' : user_id,
                'sticker' : sticker
            } 
    
            response = await self.session.post(f'{self.base_url}/uploadStickerFile', data= data)
            return response.json()

    
    
    

    async def create_download_link(self, file_path : str) -> str:


        return f'{self.download_base_url}{file_path}'
    
    
    
    async def download(self, url : str, file_name : str = None) -> bool:

        name = file_name

        if name is None:

            name = url.split('/')[-1]

    
        async with self.session.stream('GET', url) as response:
            response.raise_for_status()

            async with aiofiles.open(name, 'wb') as file:

                async for i in response.aiter_bytes(8192):

                    await file.write(i)
    
        return True

        
    



    async def _extract_user_id(self, update):
        
        try:

            user_id = update.get('message', {}).get('from', {}).get('id')
    
            if user_id is None:
    
                user_id = update.get('callback_query', {}).get('from', {}).get('id')
            if user_id is None:
                user_id = update.get('pre_checkout_query', {}).get('from', {}).get('id')
    
            if user_id is None:
                await self._process_update(update)
                return
    
            queue = self._queues.setdefault(user_id, asyncio.Queue())
    
    
            await queue.put(update)
        
        except Exception as e:
            print(f"Error while extracting user ID from update: {e}")
        
        
    


        async with self._worker_locks[user_id]:
        
            worker = self._workers.get(user_id)
            if worker and not worker.done():
                return
            self._workers[user_id] = asyncio.create_task(self._worker(user_id))
            
    

    async def _worker(self, user_id):

         
      

        while True:
            queue = self._queues.get(user_id)
            if queue is None:
                
                return
                
            try:

                update = await asyncio.wait_for(queue.get(), timeout= 180)
    
            except asyncio.TimeoutError:

                self._workers.pop(user_id, None)
                self._queues.pop(user_id, None)
                self._worker_locks.pop(user_id, None)
                return
            try:

                await self._process_update(update)
            except Exception as e:
                print(e)



    async def _get_bot_username(self):
      
      
        res = await self.get_me()
      
        if not res:
            print('invalid bot token or API error')
            return
          
        self._bot_username = res.username
        print(f'{self._bot_username} is ready to use')




    async def _process_update(self, data):

        update = Update(data, self)

        token = self._current_message.set({'chat_id' : update.chat.id,
                                           'message_id' : update.message_id})

        try:
      
            for handler_info in self.handler:
                handler_func = handler_info['func']
                filter_func = handler_info['filter']
           

                should_run = True


                if filter_func:
             
                    try:

                        for f in filter_func:

              

                            if asyncio.iscoroutinefunction(f):
                                result = await f(update)
                            else:
                                result = f(update) 

                            
                            if not result:
                                should_run = False
                                break


              
                    except Exception as e:
                        print(f"Error in filter : {e}")
                        should_run = False
                        break

                    
           
                if not should_run:
                    continue
       
                try:
                    
                    async def run(index):
                
                        if index < len(self._middlewares):
                    
                            async def call_next():
                                await run(index + 1)
                    
                            await self._middlewares[index](update, call_next)
                    
                        else:
                            await handler_func(update)
                    
                    await run(0)
                    return
                    
         
                except Exception as e:
                    print(f"Error executing handler {handler_func.__name__}: {e}")
        
        finally:
            self._current_message.reset(token)
      



    async def run(self, timeout: int = 15, sleep: float = 0.7,
                   webhook_path : str = '/webhook', host : str = '0.0.0.0', port : int = 8000):
                       
        if self.use_webhook is not True:
            
            await self._get_bot_username()
                        
            try:

                while True:
                    try:
                        data = await self.get_updates(offset = self.offset, timeout = timeout, request_timeout = timeout + 5)
                        
                        if data.get('ok'):
                            updates = data.get('result', [])
                            if not updates:
                                await asyncio.sleep(sleep)
                                continue
    
                            for i in updates:
                           
                                asyncio.create_task(self._extract_user_id(i))
    
                            
    
                            last_update = updates[-1]
                            update_id = last_update.get('update_id')
                            self.offset = update_id + 1
    
                    except httpx.TimeoutException as e:
                        print(f'timeout error : {e}')
                        await asyncio.sleep(2)
                        
                    except httpx.HTTPError as e:
                        print(f'http error : {e}')
                        await asyncio.sleep(2)
                        
                    except Exception as e:
                        print(f'exception error : {e}')
                        await asyncio.sleep(2)
            
            finally:
                                                         
                await self.session.aclose()
                        

        else :
            
            from fastapi import FastAPI, Request,BackgroundTasks
            import uvicorn

            app = FastAPI()

            @app.post(webhook_path)
            async def run_server(request:Request, back:BackgroundTasks):
                
                data = await request.json()
               

                back.add_task(self._extract_user_id, data)

                return {"ok" : True}
            
            config = uvicorn.Config(app, host=host, port=port, log_level='warning')
            server = uvicorn.Server(config)
            
            try:
                
                await self._get_bot_username()
                await server.serve()
            
            except Exception as e:
                print(f"Error while serving webhook: {e}")
                
            
            finally:
                await self.session.aclose()
                
                
            
                
            

