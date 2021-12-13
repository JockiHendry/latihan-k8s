package me.jocki.latihank8s.stockitemservice.item;

import org.springframework.amqp.core.ExchangeTypes;
import org.springframework.amqp.rabbit.annotation.Exchange;
import org.springframework.amqp.rabbit.annotation.Queue;
import org.springframework.amqp.rabbit.annotation.QueueBinding;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.stereotype.Component;

@Component
public class StockItemEventListener {

    private final StockItemViewRepository stockItemViewRepository;

    public StockItemEventListener(StockItemViewRepository stockItemViewRepository) {
        this.stockItemViewRepository = stockItemViewRepository;
    }

    @RabbitListener(bindings = @QueueBinding(
        value = @Queue, exchange = @Exchange(value = "stock-item-service.topic", type = ExchangeTypes.TOPIC), key = "event.stockItemCreated"
    ))
    public void handleStockItemCreatedEvent(StockItemCreatedEvent stockItemCreatedEvent) {
        StockItemView stockItemView = new StockItemView(stockItemCreatedEvent.getSku(), stockItemCreatedEvent.getName(),
            stockItemCreatedEvent.getCategory(), stockItemCreatedEvent.getQuantity());
        stockItemViewRepository.save(stockItemView);
    }

}
