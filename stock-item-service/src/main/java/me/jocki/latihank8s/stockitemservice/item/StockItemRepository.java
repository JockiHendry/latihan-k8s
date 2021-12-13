package me.jocki.latihank8s.stockitemservice.item;

import org.springframework.data.mongodb.repository.ReactiveMongoRepository;
import reactor.core.publisher.Mono;

public interface StockItemRepository extends ReactiveMongoRepository<StockItem, String> {

    Mono<StockItem> findBySku(String sku);

}
