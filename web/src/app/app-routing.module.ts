import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {PageNotFoundComponent} from './page-not-found-component/page-not-found.component';
import {DashboardComponent} from './dashboard/dashboard.component';
import {AutoLoginAllRoutesGuard} from 'angular-auth-oidc-client';

const routes: Routes = [
  { path: '', redirectTo: '/dashboard', pathMatch: 'full' },
  { path: 'dashboard', component: DashboardComponent, canActivate: [AutoLoginAllRoutesGuard] },
  { path: 'items', loadChildren: () => import('./stock-item/stock-item.module').then(m => m.StockItemModule), canActivate: [AutoLoginAllRoutesGuard] },
  { path: '**', component: PageNotFoundComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
