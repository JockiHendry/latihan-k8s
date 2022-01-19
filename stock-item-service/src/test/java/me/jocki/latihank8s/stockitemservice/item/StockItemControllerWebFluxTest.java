package me.jocki.latihank8s.stockitemservice.item;

import org.junit.jupiter.api.Test;
import org.springframework.amqp.core.AmqpTemplate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.autoconfigure.security.oauth2.resource.reactive.ReactiveOAuth2ResourceServerAutoConfiguration;
import org.springframework.boot.autoconfigure.security.reactive.ReactiveSecurityAutoConfiguration;
import org.springframework.boot.test.autoconfigure.web.reactive.WebFluxTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.web.reactive.server.WebTestClient;
import reactor.core.publisher.Mono;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.BDDMockito.given;
import static org.mockito.Mockito.*;

@WebFluxTest(value = StockItemController.class, excludeAutoConfiguration = {ReactiveSecurityAutoConfiguration.class, ReactiveOAuth2ResourceServerAutoConfiguration.class})
public class StockItemControllerWebFluxTest {

    @Autowired
    private WebTestClient webClient;

    @MockBean
    private StockItemRepository stockItemRepository;
    
    @MockBean
    private AmqpTemplate amqpTemplate;

    @Test
    public void create() {
        StockItemCreateRequestDto createRequestDto = new StockItemCreateRequestDto("sku1", "item1", "https://files.latihan.jocki.me/file1.img", 10L, "category1");
        StockItem stockItem = new StockItem("sku1", "item1", "https://files.latihan.jocki.me/file1.img", 10L, "category1");
        given(this.stockItemRepository.findBySku("sku1")).willReturn(Mono.empty());
        given(this.stockItemRepository.save(any())).willReturn(Mono.just(stockItem));
        this.webClient.post().uri("/items").bodyValue(createRequestDto).exchange().expectStatus().isOk()
            .expectBody(StockItemCreateResponseDto.class).isEqualTo(new StockItemCreateResponseDto(stockItem));
        verify(this.amqpTemplate, times(1)).convertAndSend("stock-item-service.topic", "event.stockItemCreated",
            new StockItemCreatedEvent("sku1", "item1", "https://files.latihan.jocki.me/file1.img", "category1", 10L));
    }

    @Test
    public void createShouldFailWhenSkuAlreadyExist() {
        StockItemCreateRequestDto createRequestDto = new StockItemCreateRequestDto("sku1", "item1", "https://files.latihan.jocki.me/file1.img", 10L, "category1");
        StockItem stockItem = new StockItem("1", "sku1", "item1", 10L, "category1");
        given(this.stockItemRepository.findBySku("sku1")).willReturn(Mono.just(stockItem));
        this.webClient.post().uri("/items").bodyValue(createRequestDto).exchange().expectStatus().is5xxServerError()
            .expectBody().jsonPath("error").isEqualTo("Product already exists");
        verify(this.amqpTemplate, never()).convertAndSend(eq("stock-item-service.topic"), eq("event.stockItemCreated"), any(StockItemCreatedEvent.class));
    }
}
