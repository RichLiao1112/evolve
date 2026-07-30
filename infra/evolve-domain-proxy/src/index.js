const UPSTREAM_ORIGIN = 'https://evolve.liveppp.com';

export default {
  async fetch(request) {
    const incoming = new URL(request.url);
    const upstream = new URL(request.url);
    upstream.protocol = 'https:';
    upstream.hostname = 'evolve.liveppp.com';
    upstream.port = '';

    const headers = new Headers(request.headers);
    headers.set('X-Forwarded-Host', incoming.host);
    headers.set('X-Forwarded-Proto', incoming.protocol.replace(':', ''));
    headers.delete('Host');

    return fetch(new Request(upstream.toString(), request, { headers }));
  },
};
