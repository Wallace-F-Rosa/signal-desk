import { Component, inject, OnInit, signal } from '@angular/core';
import { DatePipe, isPlatformBrowser } from '@angular/common';
import { PLATFORM_ID } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { Message, MessageService } from './message.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [DatePipe, FormsModule],
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class App implements OnInit {
  private readonly messageService = inject(MessageService);
  private readonly platformId = inject(PLATFORM_ID);

  protected readonly messages = signal<Message[]>([]);
  protected readonly messageText = signal('');
  protected readonly loading = signal(true);
  protected readonly submitting = signal(false);
  protected readonly error = signal('');

  ngOnInit(): void {
    if (isPlatformBrowser(this.platformId)) {
      this.loadMessages();
    }
  }

  protected loadMessages(): void {
    this.loading.set(true);
    this.error.set('');
    this.messageService.getMessages().subscribe({
      next: (messages) => {
        this.messages.set(messages);
        this.loading.set(false);
      },
      error: () => {
        this.error.set('Unable to load messages. Is the message service running?');
        this.loading.set(false);
      },
    });
  }

  protected submitMessage(): void {
    const text = this.messageText().trim();
    if (!text || this.submitting()) {
      return;
    }

    this.submitting.set(true);
    this.error.set('');
    this.messageService.createMessage({ text }).subscribe({
      next: (message) => {
        this.messages.update((messages) => [...messages, message]);
        this.messageText.set('');
        this.submitting.set(false);
      },
      error: () => {
        this.error.set('Unable to send your message. Please try again.');
        this.submitting.set(false);
      },
    });
  }
}
