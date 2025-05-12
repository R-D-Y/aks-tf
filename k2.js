import http from 'k6/http';
import { check } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 50 },  // ramp-up à 50 utilisateurs
    { duration: '1m', target: 50 },   // maintien à 50 utilisateurs
    { duration: '30s', target: 0 },   // ramp-down
  ],
};

export default function () {
  const res = http.get('http://192.168.2.2/', {
    headers: {
      'Host': 'toto.com',  // important pour que HAProxy applique son rewrite
    },
  });

  check(res, {
    'status is 200': (r) => r.status === 200,
    'body is not empty': (r) => r.body.length > 0,
  });
}