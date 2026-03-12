import TelegramBot from 'node-telegram-bot-api';
import express from 'express';

export class TelegramBotClient {
  public bot: TelegramBot;
  private token: string;

  constructor(token: string, webhookMode: boolean = false) {
    this.token = token;
    this.bot = new TelegramBot(token, {
      polling: !webhookMode,
    });
  }

  async startPolling(): Promise<void> {
    const me = await this.bot.getMe();
    console.log(`Bot @${me.username} (${me.first_name}) started with polling`);
  }

  async startWebhook(port: number, webhookUrl: string, secret?: string): Promise<void> {
    const app = express();
    app.use(express.json());

    // Webhook endpoint
    app.post(`/webhook/${this.token}`, (req, res) => {
      if (secret) {
        const headerSecret = req.headers['x-telegram-bot-api-secret-token'];
        if (headerSecret !== secret) {
          return res.sendStatus(403);
        }
      }
      this.bot.processUpdate(req.body);
      res.sendStatus(200);
    });

    // Health check
    app.get('/health', (_req, res) => {
      res.json({ status: 'ok', bot: 'running' });
    });

    // Register webhook with Telegram
    await this.bot.setWebHook(`${webhookUrl}/webhook/${this.token}`, {
      max_connections: 40,
      secret_token: secret,
    } as any);

    const info = await this.bot.getWebHookInfo();
    console.log('Webhook registered:', info.url);

    app.listen(port, () => {
      console.log(`Express server listening on port ${port}`);
    });

    const me = await this.bot.getMe();
    console.log(`Bot @${me.username} (${me.first_name}) started with webhook`);
  }

  /**
   * Send a text message with automatic retry on rate limit.
   */
  async sendMessageSafe(
    chatId: number | string,
    text: string,
    options?: TelegramBot.SendMessageOptions
  ): Promise<TelegramBot.Message | null> {
    const maxRetries = 3;
    for (let attempt = 0; attempt < maxRetries; attempt++) {
      try {
        return await this.bot.sendMessage(chatId, text, options);
      } catch (error: any) {
        if (error?.response?.statusCode === 429) {
          const retryAfter = error.response.body?.parameters?.retry_after || 5;
          console.warn(`Rate limited. Retrying after ${retryAfter}s...`);
          await new Promise((r) => setTimeout(r, retryAfter * 1000));
          continue;
        }
        if (error?.response?.statusCode === 403) {
          console.warn(`Bot blocked by user ${chatId}`);
          return null;
        }
        throw error;
      }
    }
    return null;
  }
}
