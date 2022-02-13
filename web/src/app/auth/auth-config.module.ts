import {NgModule} from '@angular/core';
import {AuthModule} from 'angular-auth-oidc-client';
import {PathUtil} from '../shared/path-util';


@NgModule({
  imports: [AuthModule.forRoot({
    config: {
      authority: PathUtil.generate('https://auth.latihan.jocki.me/auth/realms/latihan'),
      redirectUrl: window.location.origin,
      postLogoutRedirectUri: window.location.origin,
      clientId: 'latihan-k8s',
      scope: 'openid profile offline_access',
      responseType: 'code',
      silentRenew: true,
      useRefreshToken: true,
      renewTimeBeforeTokenExpiresInSeconds: 30,
      secureRoutes: [PathUtil.generate('https://api.latihan.jocki.me/')],
      }
  })],
  exports: [AuthModule],
})
export class AuthConfigModule {}
