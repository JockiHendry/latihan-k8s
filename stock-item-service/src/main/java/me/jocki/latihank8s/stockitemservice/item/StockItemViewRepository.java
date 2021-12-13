package me.jocki.latihank8s.stockitemservice.item;

import org.springframework.data.elasticsearch.repository.ElasticsearchRepository;

public interface StockItemViewRepository extends ElasticsearchRepository<StockItemView, String> {
}
