import { TelegramBotClient } from './bot-client';
import TelegramBot from 'node-telegram-bot-api';

export function registerHandlers(client: TelegramBotClient): void {
  const bot = client.bot;

  // /start command
  bot.onText(/\/start/, async (msg) => {
    const name = msg.from?.first_name || 'usuario';
    await client.sendMessageSafe(
      msg.chat.id,
      `Ola, ${name}! Bem-vindo ao bot.\n\nComandos disponiveis:\n/start - Iniciar\n/help - Ajuda\n/about - Sobre`,
      { parse_mode: 'HTML' }
    );
  });

  // /help command
  bot.onText(/\/help/, async (msg) => {
    await client.sendMessageSafe(
      msg.chat.id,
      '<b>Comandos:</b>\n' +
        '/start - Iniciar o bot\n' +
        '/help - Ver esta mensagem\n' +
        '/about - Informacoes sobre o bot\n' +
        '/echo &lt;texto&gt; - Repetir texto',
      { parse_mode: 'HTML' }
    );
  });

  // /about command
  bot.onText(/\/about/, async (msg) => {
    const me = await bot.getMe();
    await client.sendMessageSafe(
      msg.chat.id,
      `<b>${me.first_name}</b>\n@${me.username}\n\nBot criado com Telegram Bot API`,
      { parse_mode: 'HTML' }
    );
  });

  // /echo command
  bot.onText(/\/echo (.+)/, async (msg, match) => {
    const text = match?.[1] || '';
    await client.sendMessageSafe(msg.chat.id, text);
  });

  // Callback query handler (for inline keyboards)
  bot.on('callback_query', async (query) => {
    await bot.answerCallbackQuery(query.id, { text: `Opcao: ${query.data}` });

    if (query.message) {
      await bot.editMessageText(`Voce escolheu: ${query.data}`, {
        chat_id: query.message.chat.id,
        message_id: query.message.message_id,
      });
    }
  });

  // Default message handler (echo)
  bot.on('message', async (msg) => {
    // Skip commands
    if (msg.text?.startsWith('/')) return;

    // Echo non-command text messages
    if (msg.text) {
      await client.sendMessageSafe(msg.chat.id, `Voce disse: ${msg.text}`);
    }
  });

  // Error handler
  bot.on('polling_error', (error) => {
    console.error('Polling error:', error.message);
  });

  bot.on('webhook_error', (error) => {
    console.error('Webhook error:', error.message);
  });

  console.log('All handlers registered');
}
