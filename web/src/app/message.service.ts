import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Message {
  id: number;
  text: string;
  created_at: string;
  status: string;
}

export interface CreateMessage {
  text: string;
}

@Injectable({ providedIn: 'root' })
export class MessageService {
  private readonly http = inject(HttpClient);
  private readonly endpoint = 'http://localhost:8000/api/messages';

  getMessages(): Observable<Message[]> {
    return this.http.get<Message[]>(this.endpoint);
  }

  createMessage(payload: CreateMessage): Observable<Message> {
    return this.http.post<Message>(this.endpoint, payload);
  }
}
