from typing import List, Union, Dict
import json


class Update:
    __slots__ = ('update_id', 'message_id', 'date', 'text', 'author', 'chat',
                 'document', 'voice', 'entities', 'reply_to_message', 'location',
                 'contact', 'callback_query', 'new_chat_members', 'left_chat_member',
                   'pre_checkout_query', 'caption', '_bot', 'forward_origin', 'forward_from',
                     'forward_date', 'photo', 'animation', 'video', 'sticker', 'successful_payment',
                     'invoice', 'sender_chat', "_raw", 'caption_entities')

    def __init__(self, data_Message, instance):
        self._raw = data_Message
        self._bot = instance

        message_data = data_Message.get('message', {})

        self.update_id = data_Message.get('update_id')
        self.message_id = message_data.get('message_id')
        self.date = message_data.get('date')
        self.text = message_data.get('text')
        self.caption = message_data.get('caption')

        
        self.author = User(message_data.get('from', {}))
        self.chat = Chat(message_data.get('chat', {}))

        
        self.document = None
        self.voice = None
        self.entities = None
        self.reply_to_message = None
        self.location = None
        self.contact = None
        self.callback_query = None
        self.new_chat_members = None
        self.left_chat_member = None
        self.pre_checkout_query = None
        self.forward_origin = None
        self.forward_from = None
        self.forward_date = None
        self.photo = None
        self.animation = None
        self.video = None
        self.sticker = None
        self.successful_payment = None
        self.invoice = None
        self.sender_chat = None
        self.caption_entities = None

        if 'document' in message_data:
            self.document = Document(message_data['document'])

        if 'voice' in message_data:
            self.voice = Voice(message_data['voice'])

        if 'entities' in message_data:
            self.entities = Entities(message_data['entities'])

        if 'caption_entities' in message_data:
            self.caption_entities = Entities(message_data['caption_entities'])

        if 'reply_to_message' in message_data:
            self.reply_to_message = ReplyMessage(message_data['reply_to_message'])

        if 'location' in message_data:
            self.location = Location(message_data['location'])

        if 'contact' in message_data:
            self.contact = Contact(message_data['contact'])

        if 'callback_query' in data_Message:
            self.callback_query = CallbackQuery(data_Message['callback_query'])

        if 'new_chat_members' in message_data:
            self.new_chat_members = [
                User(i) for i in message_data['new_chat_members']
            ]

        if 'left_chat_member' in message_data:
            self.left_chat_member = User(message_data['left_chat_member'])

        if 'pre_checkout_query' in data_Message:
            self.pre_checkout_query = PreCheckoutQuery(
                data_Message['pre_checkout_query']
            )

        if 'forward_origin' in message_data:
            self.forward_origin = ForwardOrigin(message_data['forward_origin'])

        if 'forward_from' in message_data:
            self.forward_from = User(message_data['forward_from'])

        if 'forward_date' in message_data:
            self.forward_date = message_data['forward_date']

        if 'photo' in message_data:
            self.photo = Photo(message_data['photo'])

        if 'animation' in message_data:
            self.animation = Media(message_data['animation'])

        if 'video' in message_data:
            self.video = Media(message_data['video'])

        if 'sticker' in message_data:
            self.sticker = Sticker(message_data['sticker'])

        if 'successful_payment' in message_data:
            self.successful_payment = SuccessfulPayment(
                message_data['successful_payment']
            )

        if 'invoice' in message_data:
            self.invoice = Invoice(message_data['invoice'])

        if 'sender_chat' in message_data:

            self.sender_chat = Chat(message_data['sender_chat'])

    @property
    def user_id(self):

        user_id = self.author.id
                                        
        if user_id is None and self.callback_query is not None:

            user_id = self.callback_query.author.id


        elif user_id is None and self.pre_checkout_query is not None:

            user_id = self.pre_checkout_query.author.id

        return user_id


    @property
    def chat_id(self):

        chat_id = self.chat.id

        if chat_id is None and self.sender_chat:

            chat_id = self.sender_chat.id

        elif chat_id is None and self.callback_query:

            chat_id = self.callback_query.message.chat.id


        return chat_id


    @property
    def chat_type(self):

        chat_type = self.chat.type

        if not chat_type and self.sender_chat:

            chat_type = self.sender_chat.type

        elif not chat_type and self.callback_query:

            chat_type = self.callback_query.message.chat.type


        return chat_type



    def __str__(self):
        return json.dumps(self._raw, ensure_ascii=False, indent=4)
    
    __repr__ = __str__
        


class User:


    __slots__ = ('id', 'is_bot', 'first_name', 'last_name', 'full_name', 'username', '_raw')


    def __init__(self, data_author):

        self._raw = data_author
        
        self.id = data_author.get('id')
        self.is_bot = data_author.get('is_bot')
        self.first_name = data_author.get('first_name')
        self.last_name = data_author.get('last_name')
        self.full_name = f"{self.first_name or ''} {self.last_name or ''}".strip()
        self.username = data_author.get('username')
       
    
    def __str__(self):
        return json.dumps(self._raw, ensure_ascii=False, indent=4)
    
    __repr__ = __str__


class Chat:

    __slots__ = (
        'id',
        'type',
        'username',
        'first_name',
        'last_name',
        'full_name',
        'title',
        '_raw'
    )

    def __init__(self, data_chat):

    
        self._raw = data_chat

        self.id = data_chat.get('id')
        self.type = data_chat.get('type')
        self.username = data_chat.get('username')
        self.first_name = data_chat.get('first_name')
        self.last_name = data_chat.get('last_name')
        self.full_name = f"{self.first_name or ''} {self.last_name or ''}".strip()
        self.title = data_chat.get('title')

    def __str__(self):
        return json.dumps(self._raw, ensure_ascii=False, indent=4)

    __repr__ = __str__
    


class ReplyMessage:

    __slots__ = (
        'message_id', 'date', 'text',
        'audio', 'document', 'caption',
        'author', 'chat', '_raw', 'photo',
        'voice', 'video', 'sticker', 'animation'
    )

    def __init__(self, data_reply):

        self._raw = data_reply

        self.message_id = data_reply.get('message_id')
        self.date = data_reply.get('date')

        self.text = data_reply.get('text')
        self.caption = data_reply.get('caption')

    
        self.author = User(data_reply.get('from', {}))
        self.chat = Chat(data_reply.get('chat', {}))

        
        self.audio = None
        self.document = None
        self.photo = None
        self.voice = None
        self.video = None
        self.sticker = None
        self.animation = None

        if 'audio' in data_reply:
            self.audio = Audio(data_reply['audio'])

        if 'document' in data_reply:
            self.document = Document(data_reply['document'])

        if 'photo' in data_reply:
            self.photo = Photo(data_reply['photo'])

        if 'voice' in data_reply:
            self.voice = Voice(data_reply['voice'])

        if 'video' in data_reply:
            self.video = Media(data_reply['video'])

        if 'sticker' in data_reply:
            self.sticker = Sticker(data_reply['sticker'])

        if 'animation' in data_reply:
            self.animation = Media(data_reply['animation'])

    def __str__(self):
        return json.dumps(self._raw, ensure_ascii=False, indent=4)

    __repr__ = __str__



class Voice:


    __slots__ = ('id', 'unique_id', 'duration', 'mime_type', 'size', "_raw")


    def __init__(self, voice_data):
        
        self.id = voice_data.get('file_id')
        self.unique_id = voice_data.get('file_unique_id')
        self.duration = voice_data.get('duration')
        self.mime_type = voice_data.get('mime_type')
        self.size = voice_data.get('file_size')
        self._raw = voice_data
    
    def __str__(self):
        return json.dumps(self._raw, ensure_ascii=False, indent=4)
    
    __repr__ = __str__


class Document:


    __slots__ = ('id', 'unique_id', 'name', 'mime_type', 'size', "_raw")


    def __init__(self, data_document):
     
        self.id = data_document.get('file_id')
        self.unique_id = data_document.get('file_unique_id')
        self.name = data_document.get('file_name')
        self.mime_type = data_document.get('mime_type')
        self.size = data_document.get('file_size')
        
        self._raw = data_document
    
    def __str__(self):
        return json.dumps(self._raw, ensure_ascii=False, indent=4)
    
    __repr__ = __str__


class Location:


    __slots__ = ('longitude', 'latitude', "_raw")


    def __init__(self, location_data):
     
        self.latitude = location_data.get('latitude')
        self.longitude = location_data.get('longitude')
        self._raw = location_data
    
    def __str__(self):
        return json.dumps(self._raw, ensure_ascii=False, indent=4)
    
    __repr__ = __str__


class Contact:


    __slots__ = ('phone_number', 'first_name', 'last_name', 'user_id', "_raw")


    def __init__(self, contact_data):
      
        self.phone_number = contact_data.get('phone_number')
        self.first_name = contact_data.get('first_name')
        self.last_name = contact_data.get('last_name')
        self.user_id = contact_data.get('user_id')
        self._raw = contact_data
    
    def __str__(self):
        return json.dumps(self._raw, ensure_ascii=False, indent=4)
    
    __repr__ = __str__



class CallbackQuery:


    __slots__ = ('id', 'data', 'chat_instance', 'message', 'author', "_raw")


    def __init__(self, callback_data):
       
        self.id = callback_data.get('id')
        self.data = callback_data.get('data')
        self.chat_instance = callback_data.get('chat_instance')
        self.message = CallbackMessage(callback_data.get('message', {}))
        self.author = User(callback_data.get('from', {}))
        self._raw = callback_data
    
    def __str__(self):
        return json.dumps(self._raw, ensure_ascii=False, indent=4)
    
    __repr__ = __str__



class CallbackMessage:


    __slots__ = ('message_id', 'date', 'text', 'author', 'chat', "_raw")


    def __init__(self, data):
       
        self.message_id = data.get('message_id')
        self.date = data.get('date')
        self.text = data.get('text')
        self.author = User(data.get('from', {}))
        self.chat = Chat(data.get('chat', {}))
        self._raw = data
    
    def __str__(self):
        return json.dumps(self._raw, ensure_ascii=False, indent=4)
    
    __repr__ = __str__



class Button:
    __slots__ = ('text', 'request_contact', 'request_location')
    def __init__(self, text: str, request_contact: bool = False, request_location: bool = False):
        self.text = text
        self.request_contact = request_contact
        self.request_location = request_location
    def to_dict(self):
        return {'text': self.text, 'request_contact': self.request_contact, 'request_location': self.request_location}


class KeypadRow:
    __slots__ = ('buttons',)
    def __init__(self, buttons: List[Union[Button, str]]):
        self.buttons = buttons
    def to_list(self):
        result = []
        for btn in self.buttons:
            if isinstance(btn, Button):
                result.append(btn.to_dict())
            else:
                result.append(btn)
        return result


class Keypad:
    __slots__ = ('rows', 'one_time_keyboard', 'resize_keyboard')
    def __init__(self, rows: List[KeypadRow], one_time: bool = False, resize: bool = True):
        self.rows = rows
        self.one_time_keyboard = one_time
        self.resize_keyboard = resize
    def _build_dict(self):
        keyboard = [row.to_list() for row in self.rows]
        return {
            'keyboard': keyboard,
            'one_time_keyboard': self.one_time_keyboard,
            'resize_keyboard': self.resize_keyboard
        }
    def to_dict(self):
        return self._build_dict()
    def __str__(self):
        return json.dumps(self.to_dict())




class PreCheckoutQuery:

    __slots__ = ('id', 'currency', 'total_amount', 'invoice_payload', 'author', "_raw")

    def __init__(self, data):

        self.id = data.get('id')
        self.currency = data.get('currency')
        self.total_amount = data.get('total_amount')
        self.invoice_payload = data.get('invoice_payload')
        self.author = User(data.get('from', {}))
        self._raw = data
    
    def __str__(self):
        return json.dumps(self._raw, ensure_ascii=False, indent=4)
    
    __repr__ = __str__



class Entity:

    __slots__ = ("type", "offset", "length")

    def __init__(self, data):
        self.type = data.get("type")
        self.offset = data.get("offset")
        self.length = data.get("length")




class Entities:

    __slots__ = ("entities", "_raw")

    def __init__(self, data):
        self._raw = data
        self.entities = [Entity(i) for i in data]

    def __getitem__(self, index):
        return self.entities[index]

    def __len__(self):
        return len(self.entities)

    def __iter__(self):
        return iter(self.entities)

    def __bool__(self):
        return bool(self.entities)
    

    def __str__(self):
        return json.dumps(self._raw, ensure_ascii=False, indent=4)

    __repr__ = __str__









class ForwardOrigin:

    __slots__ = ('type', 'date', 'sender_user', "_raw")

    def __init__(self, data):

        self.type = data.get('type')
        self.date = data.get('date')

        self.sender_user = User(data.get('sender_user', {}))
        
        self._raw = data
    
    def __str__(self):
        return json.dumps(self._raw, ensure_ascii=False, indent=4)
    
    __repr__ = __str__








class PhotoSize:

    __slots__ = (
        "id",
        "unique_id",
        "width",
        "height",
        "size",
        "_raw",
    )

    def __init__(self, data):

        data = data or {}

        self.id = data.get("file_id")
        self.unique_id = data.get("file_unique_id")
        self.width = data.get("width")
        self.height = data.get("height")
        self.size = data.get("file_size")

        self._raw = data

    def __str__(self):
        return json.dumps(self._raw, ensure_ascii=False, indent=4)

    __repr__ = __str__




class Photo:

    __slots__ = ("photos", "_raw")

    def __init__(self, data):


        self._raw = data
        
        self.photos = [
            PhotoSize(photo)
            for photo in data
        ]

    def __getitem__(self, index):
        return self.photos[index]

    def __len__(self):
        return len(self.photos)

    def __iter__(self):
        return iter(self.photos)

    def __bool__(self):
        return bool(self.photos)


    def __str__(self):
        return json.dumps(self._raw, ensure_ascii=False, indent=4)

    __repr__ = __str__












class Media:

    __slots__ = ('id', 'unique_id', 'width', 'height', 'duration', 'mime_type', 'size', "_raw", "thumb")

    def __init__(self, data):
         
        
        self.id = data.get('file_id')
        self.unique_id = data.get('file_unique_id')
        self.width = data.get('width')
        self.height = data.get('height')
        self.duration = data.get('duration')
        self.mime_type = data.get('mime_type')
        self.size = data.get('file_size')
        self.thumb = Thumb(data.get('thumb', {}))
        self._raw = data
    
    def __str__(self):
        return json.dumps(self._raw, ensure_ascii=False, indent=4)
    
    __repr__ = __str__


        

class Sticker:

    __slots__ = ('id','unique_id','type','width','height','is_animated','is_video','set_name','size','thumb', "_raw")

    def __init__(self, data):

        self.id = data.get('file_id')
        self.unique_id = data.get('file_unique_id')
        self.type = data.get('type')
        self.width = data.get('width')
        self.height = data.get('height')
        self.is_animated = data.get('is_animated')
        self.is_video = data.get('is_video')
        self.set_name = data.get('set_name')
        self.size = data.get('file_size')
        
        self.thumb = Thumb(data.get('thumb', {}))
        
        self._raw = data
    
    def __str__(self):
        return json.dumps(self._raw, ensure_ascii=False, indent=4)
    
    __repr__ = __str__


class Thumb:

    __slots__ = ('id','unique_id','width','height','size', "_raw")

    def __init__(self, data):

        self.id = data.get('file_id')
        self.unique_id = data.get('file_unique_id')
        self.width = data.get('width')
        self.height = data.get('height')
        self.size = data.get('file_size')
        self._raw = data
        
    def __str__(self):
        return json.dumps(self._raw, ensure_ascii=False, indent=4)
    
    __repr__ = __str__


class SuccessfulPayment:

    __slots__ = ('currency', 'total_amount', 'invoice_payload', 'telegram_payment_charge_id', 'provider_payment_charge_id', "_raw")


    def __init__(self, data):


        self.currency = data.get('currency')
        self.total_amount = data.get('total_amount')
        self.invoice_payload = data.get('invoice_payload')
        self.telegram_payment_charge_id = data.get('telegram_payment_charge_id')
        self.provider_payment_charge_id = data.get('provider_payment_charge_id')
        self._raw = data


    def __str__(self):
        return json.dumps(self._raw, ensure_ascii=False, indent=4)
    
    __repr__ = __str__


class Invoice:

    __slots__ = ('title', 'description', 'start_parameter', 'currency', 'total_amount', "_raw")

    def __init__(self, data):
        
        self.title = data.get('title')
        self.description = data.get('description')
        self.start_parameter = data.get('start_parameter')
        self.currency = data.get('currency')
        self.total_amount = data.get('total_amount')
        self._raw = data

    def __str__(self):
        return json.dumps(self._raw, ensure_ascii=False, indent=4)
    
    __repr__ = __str__
        

class CopyTextButton:

    __slots__ = ('text')

    def __init__(self, text : str):
        
        self.text = text
    
    def to_dict(self):
        
        return {"text" : self.text}
    


class InlineButton:
    __slots__ = ('text', 'url', 'callback_data', 'copy_text', 'web_app')
    def __init__(self, text: str, url: str = None, callback_data: str = None, copy_text : Union[Dict, CopyTextButton]=None, web_app=None):
        self.text = text
        self.url = url
        self.callback_data = callback_data
        self.copy_text = copy_text
        self.web_app = web_app
    def to_dict(self):
        return {k: v for k, v in {
            'text': self.text,
            'url': self.url,
            'callback_data': self.callback_data,
            'copy_text': (
    self.copy_text.to_dict()
    if hasattr(self.copy_text, 'to_dict')
    else self.copy_text
),
            'web_app': self.web_app
        }.items() if v is not None}


class InlineRow:
    __slots__ = ('buttons',)
    def __init__(self, buttons: List[InlineButton]):
        if isinstance(buttons, InlineButton):
            buttons = [buttons]
        self.buttons = buttons
    def to_list(self):
        return [btn.to_dict() for btn in self.buttons]


class InlineKeypad:
    __slots__ = ('rows',)
    def __init__(self, rows: List[InlineRow]):
        self.rows = rows
    def to_dict(self):
        return {'inline_keyboard': [row.to_list() for row in self.rows]}
    def __str__(self):
        return json.dumps(self.to_dict())
    

class LabeledPrice:

    __slots__ = ('label', 'amount')

    def __init__(self, label : str, amount : int):
        
        self.label = label
        self.amount = amount
    
    def to_dict(self):

        return {"label" : self.label, "amount" : self.amount}
    



class ChatFullInfoPhoto:

    __slots__ = ('small_id', 'small_unique_id', 'big_id', 'big_unique_id', "_raw")

    def __init__(self, data):
        
        self.small_id = data.get('small_file_id')
        self.small_unique_id = data.get('small_file_unique_id')
        self.big_id = data.get('big_file_id')
        self.big_unique_id = data.get('big_file_unique_id')
        self._raw = data
    
    
    def __str__(self):
        return json.dumps(self._raw, ensure_ascii=False, indent=4)
    
    __repr__ = __str__
        

class ChatFullInfoSelfAcceptedGiftTypes:

    __slots__ = ('unlimited_gifts', 'limited_gifts', 'unique_gifts', 'premium_subscription', "_raw")

    def __init__(self, data):
        
        self.unlimited_gifts = data.get('unlimited_gifts')
        self.limited_gifts = data.get('limited_gifts')
        self.unique_gifts = data.get('unique_gifts')
        self.premium_subscription = data.get('premium_subscription')
        self._raw = data
        
    def __str__(self):
        return json.dumps(self._raw, ensure_ascii=False, indent=4)
    
    __repr__ = __str__



class InputMediaPhoto:
     
    __slots__ = ('media', 'caption', 'is_local_file', 'file_name'
    )

    def __init__(self, media : str, caption : str = None, is_local_file : bool = False):
        
        self.caption = caption
        self.media = media
        self.is_local_file = is_local_file

        self.file_name = media if is_local_file else None
    
    def to_dict(self):

        result = {"type" : "photo"}

        if self.is_local_file:
     
            name = self.file_name or "file"

            result["media"] = f"attach://{name}"
        else:
            result["media"] = self.media

        if self.caption is not None:
            result["caption"] = self.caption

        return result
   



class Audio:

    __slots__ = (
        'id',
        'unique_id',
        'duration',
        'title',
        'name',
        'mime_type',
        'size',
         "_raw"
    )

    def __init__(self, data):

        self.id = data.get('file_id')
        self.unique_id = data.get('file_unique_id')
        self.duration = data.get('duration')
        self.title = data.get('title')
        self.name = data.get('file_name')
        self.mime_type = data.get('mime_type')
        self.size = data.get('file_size')
        self._raw = data
    
    def __str__(self):
        return json.dumps(self._raw, ensure_ascii=False, indent=4)
    
    __repr__ = __str__
    



class ChatFullInfo:

    __slots__ = ('ok', 'id', 'type', 'title', 'username', 'accent_color_id',
                  'max_reaction_count', 'photo', 'accepted_gift_types', 'description',
                    'invite_link', "_raw", 'error_code', 'error_description', 'first_name',
                      'bio', 'linked_chat_id')

    def __init__(self, data):
 
 
        self.ok = data.get('ok')
        self.error_code = data.get('error_code')
        self.error_description = data.get('description')
                


        result = data.get('result') or {}
  
        self.id = result.get('id')
        self.type = result.get('type')
        self.title = result.get('title')
        self.username = result.get('username')
        self.accent_color_id = result.get('accent_color_id')
        self.max_reaction_count = result.get('max_reaction_count')
        self.photo = ChatFullInfoPhoto(result.get('photo', {}))
        self.accepted_gift_types = ChatFullInfoSelfAcceptedGiftTypes(result.get('accepted_gift_types', {}))
        self.description = result.get('description')
        self.invite_link = result.get('invite_link')
        self.first_name = result.get('first_name')
        self.bio = result.get('bio')
        self.linked_chat_id = result.get('linked_chat_id')
        self._raw = data
    
    def __str__(self):
        return json.dumps(self._raw, ensure_ascii=False, indent=4)
    
    __repr__ = __str__




class File:

    __slots__ = ('ok', 'id', 'unique_id', 'size', 'path', "_raw", 'error_code', 'error_description')

    def __init__(self, data):
           
        self.ok = data.get('ok')
        self.error_code = data.get('error_code')
        self.error_description = data.get('description')
        


        result = data.get('result') or {}
        self.id = result.get('file_id')
        self.unique_id = result.get('file_unique_id')
        self.size = result.get('file_size')
        self.path = result.get('file_path')
        self._raw = data
    
    def __str__(self):
        return json.dumps(self._raw, ensure_ascii=False, indent=4)
    
    __repr__ = __str__


    

class GetMeResponse:

    __slots__ = (
        'ok',
        'id',
        'is_bot',
        'first_name',
        'last_name',
        'full_name',
        'username',
        '_raw',
        'error_code',
        'error_description'
    )

    def __init__(self, data):

        self.ok = data.get("ok")
        self.error_code = data.get('error_code')
        self.error_description = data.get('description')


        result = data.get("result") or {}

        self.id = result.get("id")
        self.is_bot = result.get("is_bot")
        self.first_name = result.get("first_name")
        self.last_name = result.get("last_name")
        self.full_name = f"{self.first_name or ''} {self.last_name or ''}".strip()
        self.username = result.get("username")
        self._raw = data
    
    def __str__(self):
        return json.dumps(self._raw, ensure_ascii=False, indent=4)
    
    __repr__ = __str__


class MessageResponse:

    __slots__ = (
        'ok',
        'message_id',
        'author',
        'date',
        'chat',
        'text',
        'forward_date',
        'invoice',
        '_raw',
        'error_code',
        'error_description'
    )

    def __init__(self, data):

        self.ok = data.get("ok")
        self.error_code = data.get("error_code")
        self.error_description = data.get("description")

        result = data.get("result") or {}

        self.message_id = result.get("message_id")
        self.author = User(result.get("from", {}))
        self.date = result.get("date")
        self.chat = Chat(result.get("chat", {}))
        self.text = result.get("text")
        self.forward_date = result.get("forward_date")

        self.invoice = None

        if "invoice" in result:
            self.invoice = Invoice(result["invoice"])

        self._raw = data

    def __str__(self):
        return json.dumps(self._raw, ensure_ascii=False, indent=4)

    __repr__ = __str__
    
    

class ChatAdministrator:

    __slots__ = (
        "status",
        "user",
        "is_anonymous",
        "can_be_edited",
        "can_manage_chat",
        "can_delete_messages",
        "can_manage_video_chats",
        "can_restrict_members",
        "can_promote_members",
        "can_change_info",
        "can_invite_users",
        "can_pin_messages",
        "can_manage_topics",
        "_raw",
    )

    def __init__(self, data):

        data = data or {}

        self.status = data.get("status")
        self.user = User(data.get("user", {}))

        self.is_anonymous = data.get("is_anonymous")
        self.can_be_edited = data.get("can_be_edited")
        self.can_manage_chat = data.get("can_manage_chat")
        self.can_delete_messages = data.get("can_delete_messages")
        self.can_manage_video_chats = data.get("can_manage_video_chats")
        self.can_restrict_members = data.get("can_restrict_members")
        self.can_promote_members = data.get("can_promote_members")
        self.can_change_info = data.get("can_change_info")
        self.can_invite_users = data.get("can_invite_users")
        self.can_pin_messages = data.get("can_pin_messages")
        self.can_manage_topics = data.get("can_manage_topics")

        self._raw = data

    def __str__(self):
        return json.dumps(self._raw, ensure_ascii=False, indent=4)

    __repr__ = __str__
    
    

class ChatAdministratorsResponse:

    __slots__ = ("ok", "administrators", "_raw", 'error_code', 'error_description')

    def __init__(self, data):

        self.ok = data.get("ok")
        self.error_code = data.get('error_code')
        self.error_description = data.get('description')

        self.administrators = [
            ChatAdministrator(admin)
            for admin in data.get("result", [])
        ]

        self._raw = data
    
    def __getitem__(self, index):
        return self.administrators[index]

    def __len__(self):
        return len(self.administrators)
    
    def __iter__(self):
        return iter(self.administrators)
    
    def __str__(self):
        return json.dumps(self._raw, ensure_ascii=False, indent=4)

    __repr__ = __str__
    
   
     
class ChatMember:

    __slots__ = (
        'ok',
        'status',
        'user',
        'is_anonymous',
        '_raw',
        'error_code',
        'error_description'
    )

    def __init__(self, data):

        self.ok = data.get('ok')
        self.error_code = data.get('error_code')
        self.error_description = data.get('description')

        result = data.get('result') or {}

        self.status = result.get('status')
        self.user = User(result.get('user', {}))
        self.is_anonymous = result.get('is_anonymous')

        self._raw = data

    def __str__(self):
        return json.dumps(self._raw, ensure_ascii=False, indent=4)

    __repr__ = __str__



class EditedMessage:

    __slots__ = (
        "ok",
        "message_id",
        "date",
        "edit_date",
        "chat",
        'author',
        'reply_markup',
        "_raw",
        'error_code',
        'error_description'
    )

    def __init__(self, data):
        self.ok = data.get("ok")
        self.error_code = data.get('error_code')
        self.error_description = data.get('description')

        result = data.get("result") or {}

        self.message_id = result.get("message_id")
        self.author = User(result.get('from', {}))
        self.date = result.get("date")
        self.edit_date = result.get("edit_date")
        self.chat = Chat(result.get("chat", {}))
        self.reply_markup = result.get('reply_markup', {})

        self._raw = data

    def __str__(self):
        return json.dumps(self._raw, ensure_ascii=False, indent=4)

    __repr__ = __str__



class WebhookInfo:

    __slots__ = (
        "ok",
        "url",
        "has_custom_certificate",
        "pending_update_count",
        "_raw",
        'error_code',
        'error_description'
    )

    def __init__(self, data):

        self.ok = data.get("ok")
        self.error_code = data.get('error_code')
        self.error_description = data.get('description')

        result = data.get("result") or {}

        self.url = result.get("url")
        self.has_custom_certificate = result.get("has_custom_certificate")
        self.pending_update_count = result.get("pending_update_count")

        self._raw = data

    def __str__(self):
        return json.dumps(self._raw, ensure_ascii=False, indent=4)

    __repr__ = __str__



class SendMediaResult:

    __slots__ = (
        "ok",
        "message_id",
        "author",
        "date",
        "chat",
        "photo",
        "_raw",
        "document",
        "audio",
        "video",
        "animation",
        "voice",
        "media_group_id",
        "error_code",
        "error_description"
    )

    def __init__(self, data):

        self._raw = data

        self.ok = data.get("ok")
        self.error_code = data.get("error_code")
        self.error_description = data.get("description")

        result = data.get("result", {})

        self.message_id = result.get("message_id")
        self.author = User(result.get("from", {}))
        self.date = result.get("date")
        self.chat = Chat(result.get("chat", {}))

        self.photo = None
        self.document = None
        self.audio = None
        self.video = None
        self.animation = None
        self.voice = None

        if "photo" in result:
            self.photo = Photo(result["photo"])

        if "document" in result:
            self.document = Document(result["document"])

        if "audio" in result:
            self.audio = Audio(result["audio"])

        if "video" in result:
            self.video = Media(result["video"])

        if "animation" in result:
            self.animation = Media(result["animation"])

        if "voice" in result:
            self.voice = Voice(result["voice"])

        self.media_group_id = result.get("media_group_id")


class SendMediaGroupResult:

    __slots__ = (
        "ok",
        "messages",
        "_raw",
        'error_code',
        'error_description'
    )

    def __init__(self, data):

        self._raw = data

        self.ok = data.get("ok")
        self.error_code = data.get('error_code')
        self.error_description = data.get('description')

        self.messages = [
            SendMediaResult({
                "ok": self.ok,
                "result": message
            })
            for message in data.get("result", [])
        ]

    def __getitem__(self, index):
        return self.messages[index]

    def __len__(self):
        return len(self.messages)

    def __iter__(self):
        return iter(self.messages)

    def __str__(self):
        return json.dumps(self._raw, ensure_ascii=False, indent=4)

    __repr__ = __str__


class ApiResponse:

    __slots__ = ('ok', 'error_code', 'error_description', '_raw')

    def __init__(self, data):

        self._raw = data

        self.ok = data.get('ok')
        self.error_code = data.get('error_code')
        self.error_description = data.get('description')

    def __str__(self):
        return json.dumps(self._raw, ensure_ascii=False, indent=4)


    