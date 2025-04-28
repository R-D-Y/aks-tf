import http from 'k6/http';
import { check, sleep } from 'k6';
import { Trend, Rate } from 'k6/metrics';

// Définir des métriques personnalisées
const myDuration = new Trend('temps_reponse_http');
const myFailRate = new Rate('taux_erreur_http');
const mySuccessRate = new Rate('taux_succes_http');

export const options = {
  vus: 10,             // 10 utilisateurs virtuels
  duration: '30s',     // pendant 30 secondes
  thresholds: {
    'taux_succes_http': ['rate>0.95'], // On veut que 95% des requêtes réussissent
    'temps_reponse_http': ['p(95)<500'], // 95% des réponses en moins de 500ms
  },
};

export default function () {
  const proxyUrl = 'http://1.1.1.1:1111';
  const url = 'https://github.com'; // ou ton serveur interne si possible

  const res = http.get(url, { proxy: proxyUrl });

  // Ajout de métriques personnalisées
  myDuration.add(res.timings.duration);
  myFailRate.add(res.status !== 200);
  mySuccessRate.add(res.status === 200);

  // Vérifications classiques
  check(res, {
    'statut est 200': (r) => r.status === 200,
    'durée réponse < 500ms': (r) => r.timings.duration < 500,
  });

  sleep(1); // Petite pause pour éviter de spammer trop vite
}