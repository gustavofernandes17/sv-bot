import logging

from recorder import Recorder 
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from threading import Thread
from os import listdir, remove 
from os.path import isfile, join

    # token = get_token(os.getcwd() + '/token.json')

    # updater = Updater(token, use_context=True)

    # updater.dispatcher.add_handler(MessageHandler(Filters.text, echo))

    # updater.start_polling()
    # updater.idle()


class SimovTelegram():

    def __init__(self, token: str, conection_status, simov_recorder: Recorder, configurator) -> None:
        """configura o bot e incializa as configurações de depuração"""
        
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO
        )

        self.logger = logging.getLogger(__name__)

        self.token = token
        self.updater = Updater(self.token, use_context=True)
        self.dispatcher = self.updater.dispatcher


        self.conection_status = conection_status
        self.simov_recorder = simov_recorder
        self.configurator = configurator


    def init(self):
        
        self.dispatcher.add_handler(CommandHandler('gravar', self.start_recording))
        self.dispatcher.add_handler(CommandHandler('capturar', self.capture))
        self.dispatcher.add_handler(CommandHandler('status', self.status))
        self.dispatcher.add_handler(CommandHandler('config', self.config))
        self.dispatcher.add_handler(CommandHandler('parar', self.stop))

        self.updater.start_polling()
        self.updater.idle()

    def start_recording(self, update, context):
        """um comando para o servidor começar a gravar capturas da esp"""
        
        chat_id = update.effective_chat.id

        context.bot.send_message(chat_id=chat_id, text='Iniciando Gravação')

        def record_routine():
            try:    
                self.simov_recorder.capture_buffers()
            except:
                context.bot.send_message(chat_id=chat_id, text='Um erro ocorreu!') 
                context.bot.send_message(chat_id=chat_id, text='Verifique se o seu Simov está conectado à internet, ou se a conexão foi devidademente tunelada!')
        
        new_thread = Thread(target=record_routine)
        new_thread.start()
        

    
    def stop(self, update, context):

        context.bot.send_message(chat_id=update.effective_chat.id, text='Parando Gravação')
        
        try: 
            self.simov_recorder.stop_recording()

            context.bot.send_message(chat_id=update.effective_chat.id, text='Gravação Terminada')
            
            if len(self.simov_recorder.errors) == 0: 
                context.bot.send_message(chat_id=update.effective_chat.id, text='não houve erros durante a gravação')
            else:
                for error in self.simov_recorder.errors:
                    context.bot.send_message(chat_id=update.effective_chat.id, text=error)

            filenames = [f for f in listdir(self.simov_recorder.video_path) if isfile(join(self.simov_recorder.video_path, f))]
            
            with open(self.simov_recorder.video_path + '/' + filenames[0], 'rb') as video_file: 

                context.bot.send_video(
                    chat_id=update.effective_chat.id,
                    video=video_file, 
                )
            
            remove(self.simov_recorder.video_path + '/' + filenames[0])
          
        except: 
            context.bot.send_message(
                chat_id=update.effective_chat.id, 
                text="Um erro ocorreu!, você tem certeza que iniciou a gravação?"
            )

       


    def capture(self, update, context): 
        """um comando para retirar uma foto (captura) e envia-lá pelo bot"""
        pass

    def status(self, update, context):
        """envia o estado atual da camera (qualidade e resolução selecionada)"""
        pass

    def config(self, update, context):
        """altera a configuração da câmera (qualidade e resolução)"""
        pass
