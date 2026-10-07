import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Zone } from '../models/zone';
import { Estimation } from '../models/estimation';
import { environment } from '../../environment';
/*import { predictionResponse } from 'route du gateway';*/



@Injectable({ providedIn: 'root' })
export class TripService {
  private http = inject(HttpClient);
  private apiUrl = `${environment.apiBaseUrl}/prediction`;

  getZones(): Observable<Zone[]> {
    return this.http.get<Zone[]>(`${this.apiUrl}/zones`);
  }

  estimer(departId: number, arriveeId: number, dateDepart: string): Observable<Estimation> {
    return this.http.post<Estimation>(`${this.apiUrl}/estimation`, {
      departId,
      arriveeId,
      dateDepart,
    });
  }
}