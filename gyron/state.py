from time import time
import asyncio

class StateManager:

    __slots__ = (
        'auto_clear',
        '_states',
        '_cleanup_task'
    )

    def __init__(self, auto_clear: bool = True):

      
        self.auto_clear = auto_clear
        self._states = {}
        self._cleanup_task = None


        

    async def set_state_for(self, update, state, expire : int = 30):

        if expire <= 0:
            raise ValueError("expire must be greater than 0")

        if self.auto_clear and self._cleanup_task is None:

            self._cleanup_task = asyncio.create_task(self._cleanup_loop())

        expires_at = time() + expire
  

        self._states[update.author.id] = {
            'state': state,
            'expires_at': expires_at
        }

        
       

    async def clear_state_for(self, update):

        self._states.pop(update.author.id, None)

    async def get_state_for(self, update):

        data = self._states.get(update.author.id)

        if not data:
            return None

        expires_at = data['expires_at']

        if time() > expires_at:

            if self.auto_clear:
                self._states.pop(update.author.id, None)

            return None

        return data['state']
    
    async def _cleanup_loop(self):

        try:

            while True:

                now = time()

                expired = [
                k for k, v in self._states.items()
                if v['expires_at'] <= now]

                for k in expired:
                    self._states.pop(k, None)
                    
                await asyncio.sleep(20)


        finally:
            self._cleanup_task = None

