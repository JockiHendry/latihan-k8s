import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {StockItem} from './stock-item';
import {map, Observable} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class StockItemService {

  constructor(private http: HttpClient) {}

  createNewItem(stockItem: StockItem): Observable<StockItem> {
    return this.http.post<StockItem>('https://latihan.jocki.me/stock-item-service/items', stockItem);
  }

  search(keyword: string, categories: string[]): Observable<SearchResult> {
    const query: any = {
      size: 20,
      query: {
        bool: {
          must: [{
            multi_match: {
              query: keyword,
              fuzziness: 'AUTO',
              zero_terms_query: 'all',
              fields: ['name', 'sku^3']
            }
          }],
        }
      },
      highlight: {
        fields: {
          name: {},
          sku: {},
        }
      },
      aggs: {
        categories: {
          terms: {
            field: 'category.keyword',
            size: 20,
          }
        }
      }
    };
    if (categories.length > 0) {
      query.query.bool.must.push({
        terms: {
          category: categories.map(c => c.toLowerCase()),
        }
      });
    }
    return this.http.post('https://latihan.jocki.me/search/stock-item/_search', query).pipe(
      map((response: any) => {
        return {
            items: response.hits?.hits?.map((h: any) => ({...h._source, ...h.highlight} as StockItem)) ?? [],
            categories: response.aggregations?.categories?.buckets ?? [],
        } as SearchResult
      })
    )
  }

}

export interface SearchResult {

  items: StockItem[];
  categories: {key: string, doc_count: number}[];

}
