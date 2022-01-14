import {Component, OnInit, ViewChild} from '@angular/core';
import {OidcSecurityService} from 'angular-auth-oidc-client';
import {MatSidenav} from '@angular/material/sidenav';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {

  userData: any;
  @ViewChild('sidenav') sideNav: MatSidenav|null = null;

  constructor(public oidcSecurityService: OidcSecurityService) {
  }

  ngOnInit() {
    this.oidcSecurityService.userData$.subscribe((result) => {
      if (result?.userData) {
        this.userData = result.userData;
      }
    });
  }

  logout() {
    this.oidcSecurityService.logoff();
  }

  toggle() {
    this.sideNav?.toggle();
  }

}
