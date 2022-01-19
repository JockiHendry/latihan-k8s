import {Component} from '@angular/core';
import {FormBuilder, Validators} from '@angular/forms';
import {StockItemService} from '../stock-item.service';
import {MatSnackBar} from '@angular/material/snack-bar';

@Component({
  selector: 'app-create-stock-item',
  templateUrl: './create-stock-item.component.html',
  styleUrls: ['./create-stock-item.component.css']
})
export class CreateStockItemComponent {

  form = this.fb.group({
    sku: ['', Validators.required],
    name: ['', Validators.required],
    itemImage: [''],
    category: ['', Validators.required],
    quantity: [0, Validators.min(0)],
  });

  constructor(private fb: FormBuilder, private stockItemService: StockItemService, private snackbar: MatSnackBar) {}

  save() {
    if (!this.form.valid) {
      this.snackbar.open('Maaf, data masih belum terisi dengan benar.');
      return;
    }
    this.stockItemService.createNewItem(this.form.value).subscribe({
      next: (result) => {
        this.snackbar.open(`Item ${result.name} berhasil ditambahkan.`);
        this.form.reset({}, {onlySelf: true});
      },
      error: (errResponse) => {
        console.log(errResponse);
        this.snackbar.open(errResponse?.error?.error ?? errResponse.message);
      }
    });
  }

}
