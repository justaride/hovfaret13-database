import { RATE_LIMIT, RETRY_ATTEMPTS, RETRY_DELAY } from './config.js';

class RateLimiter {
  constructor(requestsPerSecond = RATE_LIMIT) {
    this.interval = 1000 / requestsPerSecond;
    this.lastRequest = 0;
  }

  async wait() {
    const now = Date.now();
    const elapsed = now - this.lastRequest;
    if (elapsed < this.interval) {
      await new Promise(r => setTimeout(r, this.interval - elapsed));
    }
    this.lastRequest = Date.now();
  }
}

export const rateLimiter = new RateLimiter();

export async function withRetry(fn, context = '') {
  for (let attempt = 1; attempt <= RETRY_ATTEMPTS; attempt++) {
    try {
      await rateLimiter.wait();
      return await fn();
    } catch (error) {
      const isRateLimited = error.code === 'rate_limited' || error.status === 429;
      const isLastAttempt = attempt === RETRY_ATTEMPTS;

      if (isRateLimited && !isLastAttempt) {
        const retryAfter = error.headers?.['retry-after'] || RETRY_DELAY * attempt;
        console.log(`Rate limited${context ? ` (${context})` : ''}. Retry ${attempt}/${RETRY_ATTEMPTS} in ${retryAfter}ms`);
        await new Promise(r => setTimeout(r, retryAfter));
      } else if (isLastAttempt) {
        throw error;
      } else if (error.code === 'conflict_error') {
        console.log(`Conflict${context ? ` (${context})` : ''}. Retry ${attempt}/${RETRY_ATTEMPTS}`);
        await new Promise(r => setTimeout(r, RETRY_DELAY * attempt));
      } else {
        throw error;
      }
    }
  }
}
