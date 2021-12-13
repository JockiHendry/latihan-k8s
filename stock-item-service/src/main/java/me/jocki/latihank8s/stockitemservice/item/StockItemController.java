package me.jocki.latihank8s.stockitemservice.item;

import org.springframework.amqp.core.AmqpTemplate;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Mono;

import java.util.Collections;
import java.util.Map;

@RestController
@RequestMapping("/items")
public class StockItemController {

    private final StockItemRepository stockItemRepository;
    private final AmqpTemplate amqpTemplate;

    public StockItemController(StockItemRepository stockItemRepository, AmqpTemplate amqpTemplate) {
        this.stockItemRepository = stockItemRepository;
        this.amqpTemplate = amqpTemplate;
    }

    @ExceptionHandler
    public ResponseEntity<Map<String, String>> handle(RuntimeException ex) {
        return ResponseEntity.internalServerError().contentType(MediaType.APPLICATION_JSON)
            .body(Collections.singletonMap("error", ex.getMessage()));
    }

    @PostMapping
    public Mono<StockItemCreateRequestDto> create(@RequestBody StockItemCreateRequestDto createRequestDto) {
        return this.stockItemRepository.findBySku(createRequestDto.getSku())
            .flatMap(__ -> Mono.error(new RuntimeException("Product already exists")))
            .switchIfEmpty(Mono.fromCallable(() -> {
                var command = new CreateStockItemCommand(createRequestDto.getSku(), createRequestDto.getName(), createRequestDto.getQuantity(), createRequestDto.getCategory());
                amqpTemplate.convertAndSend("stock-item-service.topic", "command.createStockItem", command);
                return createRequestDto;
            }))
            .cast(StockItemCreateRequestDto.class);
    }

}
