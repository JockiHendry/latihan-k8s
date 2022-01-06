package me.jocki.latihank8s.stockitemservice.item;

import org.springframework.data.elasticsearch.repository.ElasticsearchRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface StockItemViewRepository extends ElasticsearchRepository<StockItemView, String> {
}
