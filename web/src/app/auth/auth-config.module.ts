import { NgModule } from '@angular/core';
import { AuthModule } from 'angular-auth-oidc-client';


@NgModule({
    imports: [AuthModule.forRoot({
        config: {
              authority: 'http://auth.jocki.me/auth/realms/latihan',
              redirectUrl: window.location.origin,
              postLogoutRedirectUri: window.location.origin,
              clientId: 'latihan-k8s',
              scope: 'openid profile offline_access',
              responseType: 'code',
              silentRenew: true,
              useRefreshToken: true,
              renewTimeBeforeTokenExpiresInSeconds: 30,
              secureRoutes: ['https://latihan.jocki.me/'],
          }
      })],
    exports: [AuthModule],
})
export class AuthConfigModule {}
