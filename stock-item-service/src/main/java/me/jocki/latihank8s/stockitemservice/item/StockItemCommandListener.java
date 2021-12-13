package me.jocki.latihank8s.stockitemservice.item;

import org.springframework.amqp.AmqpRejectAndDontRequeueException;
import org.springframework.amqp.core.AmqpTemplate;
import org.springframework.amqp.core.ExchangeTypes;
import org.springframework.amqp.rabbit.annotation.Exchange;
import org.springframework.amqp.rabbit.annotation.Queue;
import org.springframework.amqp.rabbit.annotation.QueueBinding;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.stereotype.Component;
import reactor.core.publisher.Mono;

@Component
public class StockItemCommandListener {

    private final StockItemRepository stockItemRepository;
    private final AmqpTemplate amqpTemplate;

    public StockItemCommandListener(StockItemRepository stockItemRepository, AmqpTemplate amqpTemplate) {
        this.stockItemRepository = stockItemRepository;
        this.amqpTemplate = amqpTemplate;
    }

    @RabbitListener(bindings = @QueueBinding(
        value = @Queue, exchange = @Exchange(value = "stock-item-service.topic", type = ExchangeTypes.TOPIC), key = "command.createStockItem"
    ))
    public void handleCreateStockItemCommand(CreateStockItemCommand command) {
        stockItemRepository.findBySku(command.getSku())
            .flatMap(__ -> Mono.error(new AmqpRejectAndDontRequeueException("Product already exists")))
            .switchIfEmpty(stockItemRepository.save(new StockItem(null, command.getSku(), command.getName(), command.getQuantity(), command.getCategory())))
            .cast(StockItem.class)
            .subscribe(s -> amqpTemplate.convertAndSend("stock-item-service.topic", "event.stockItemCreated",
                new StockItemCreatedEvent(s.getSku(), s.getName(), s.getCategory(), s.getQuantity())));
    }

}
