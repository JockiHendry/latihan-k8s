package me.jocki.latihank8s.stockitemservice.item;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@NoArgsConstructor @AllArgsConstructor @Data
public class StockItemCreatedEvent {

    private String sku;
    private String name;
    private String category;
    private Long quantity;

}
