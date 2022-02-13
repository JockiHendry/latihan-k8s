export class PathUtil {

  static getTenantId(): string|null {
    const hostname = window.location.hostname.split('.')[0];
    const parts = hostname.split('-');
    if (parts.length === 1) {
      return null;
    }
    return parts.pop() ?? null;
  }

  static generate(basePath: string): string {
    const tenantId = this.getTenantId();
    if (tenantId == null) {
      return basePath;
    }
    const url = new URL(basePath)
    const parts = url.hostname.split('.');
    parts[0] = `${parts[0]}-${tenantId}`;
    url.hostname = parts.join('.');
    return url.toString();
  }

}
