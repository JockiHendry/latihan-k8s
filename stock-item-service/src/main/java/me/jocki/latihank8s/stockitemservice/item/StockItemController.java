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
    public Mono<StockItemCreateResponseDto> create(@RequestBody StockItemCreateRequestDto createRequestDto) {
        return this.stockItemRepository.findBySku(createRequestDto.getSku())
            .hasElement()
            .flatMap(v -> {
                if (v) {
                    return Mono.error(new RuntimeException("Product already exists"));
                }
                return stockItemRepository.save(new StockItem(createRequestDto.getSku(), createRequestDto.getName(),
                        createRequestDto.getItemImage(), createRequestDto.getQuantity(), createRequestDto.getCategory()));
            })
            .map(s -> {
                amqpTemplate.convertAndSend("stock-item-service.topic", "event.stockItemCreated",
                        new StockItemCreatedEvent(s.getSku(), s.getName(), s.getItemImage(), s.getCategory(), s.getQuantity()));
                return new StockItemCreateResponseDto(s);
            });
    }

}
