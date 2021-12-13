import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {ListStockItemComponent} from './list-stock-item/list-stock-item.component';
import {CreateStockItemComponent} from './create-stock-item/create-stock-item.component';

const routes: Routes = [
  { path: '', component: ListStockItemComponent },
  { path: 'create', component: CreateStockItemComponent },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class StockItemRoutingModule { }
