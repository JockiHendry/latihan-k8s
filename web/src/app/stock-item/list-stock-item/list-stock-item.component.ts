import {Component, OnDestroy, OnInit} from '@angular/core';
import {StockItemService} from '../stock-item.service';
import {StockItem} from '../stock-item';
import {MatSelectionListChange} from '@angular/material/list';
import {FormControl} from '@angular/forms';
import {Subscription} from 'rxjs';

@Component({
  selector: 'app-list-stock-item',
  templateUrl: './list-stock-item.component.html',
  styleUrls: ['./list-stock-item.component.css']
})
export class ListStockItemComponent implements OnInit, OnDestroy {

  displayedColumns: string[] = ['id', 'name', 'category', 'quantity'];
  dataSource: StockItem[] = [];
  categories: {key: string, doc_count: number}[] = [];
  selectedCategories: string[] = [];
  searchControl = new FormControl('');

  private searchControlSubscription: Subscription;

  constructor(private stockItemService: StockItemService) {
    this.searchControlSubscription = this.searchControl.valueChanges.subscribe(() => {
      this.search();
    })
  }

  ngOnInit(): void {
    this.search();
  }

  ngOnDestroy() {
    this.searchControlSubscription?.unsubscribe();
  }

  onCategorySelectionChanged(event: MatSelectionListChange) {
    this.selectedCategories = event.source.selectedOptions.selected.map(o => o.value);
    this.search()
  }

  search() {
    this.stockItemService.search(this.searchControl.value, this.selectedCategories).subscribe((result) => {
      this.dataSource = result.items;
      this.categories = result.categories;
    });
  }

}
