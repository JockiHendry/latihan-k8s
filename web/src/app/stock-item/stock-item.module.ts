import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ListStockItemComponent } from './list-stock-item/list-stock-item.component';
import {StockItemRoutingModule} from './stock-item-routing.module';
import {MatCardModule} from '@angular/material/card';
import {MatTableModule} from '@angular/material/table';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatInputModule} from '@angular/material/input';
import {MatIconModule} from '@angular/material/icon';
import { CreateStockItemComponent } from './create-stock-item/create-stock-item.component';
import {MatButtonModule} from '@angular/material/button';
import {FlexModule} from '@angular/flex-layout';
import {ReactiveFormsModule} from '@angular/forms';
import {MatSnackBarModule} from '@angular/material/snack-bar';
import {MatListModule} from '@angular/material/list';
import {MatBadgeModule} from '@angular/material/badge';
import {SharedModule} from '../shared/shared.module';



@NgModule({
  declarations: [
    ListStockItemComponent,
    CreateStockItemComponent
  ],
    imports: [
        CommonModule,
        StockItemRoutingModule,
        MatCardModule,
        MatTableModule,
        MatFormFieldModule,
        MatInputModule,
        MatIconModule,
        MatButtonModule,
        MatSnackBarModule,
        FlexModule,
        ReactiveFormsModule,
        MatListModule,
        MatBadgeModule,
        SharedModule,
    ]
})
export class StockItemModule { }
