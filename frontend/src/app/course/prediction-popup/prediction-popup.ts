import { Component, OnInit, inject, signal, PLATFORM_ID } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { DatePipe, isPlatformBrowser  } from '@angular/common';
import { TripService } from '../../services/prediction-popup';
import { Zone } from '../../models/zone';
import { Resultat } from '../../models/resultat';

@Component({
  selector: 'app-trip-popup',
  standalone: true,
  imports: [FormsModule, DatePipe],
  templateUrl: './prediction-popup.html',
  styleUrl: './prediction-popup.scss',
})
export class PredictionPopupComponent implements OnInit {
  private tripService = inject(TripService);
  private platformId = inject(PLATFORM_ID);

  ouvert = signal(false);
  zones = signal<Zone[]>([]);
  resultat = signal<Resultat | null>(null);
  chargement = signal(false);
  erreur = signal('');

  departId: number | null = null;
  arriveeId: number | null = null;
  dateDepart = '';

  ngOnInit() {
    if (isPlatformBrowser(this.platformId)) {
      this.tripService.getZones().subscribe({
        next: (zones) => this.zones.set(zones),
        error: () => this.erreur.set('Impossible de charger les zones'),
      });
    }
  }

  ouvrir() {
    this.ouvert.set(true);
  }

  fermer() {
    this.ouvert.set(false);
    this.resultat.set(null);
    this.erreur.set('');
  }

  valider() {
    if (!this.departId || !this.arriveeId || !this.dateDepart) {
      this.erreur.set('Merci de remplir tous les champs');
      return;
    }

    this.erreur.set('');
    this.chargement.set(true);

    this.tripService.estimer(this.departId, this.arriveeId, this.dateDepart).subscribe({
      next: (estimation) => {
        const depart = new Date(this.dateDepart);
        const arrivee = new Date(depart.getTime() + estimation.dureeMinutes * 60000);

        this.resultat.set({
          depart: this.nomZone(this.departId!),
          arrivee: this.nomZone(this.arriveeId!),
          dateDepart: depart,
          dateArrivee: arrivee,
          duree: estimation.dureeMinutes,
        });
        this.chargement.set(false);
      },
      error: () => {
        this.erreur.set("Erreur lors du calcul de l'arrivée");
        this.chargement.set(false);
      },
    });
  }

  private nomZone(id: number): string {
    return this.zones().find((z) => z.id === id)?.nom ?? '';
  }
}