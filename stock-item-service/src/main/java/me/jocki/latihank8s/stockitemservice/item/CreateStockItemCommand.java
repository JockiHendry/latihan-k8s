package me.jocki.latihank8s.stockitemservice.item;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@NoArgsConstructor @AllArgsConstructor @Data
public class CreateStockItemCommand {

    private String sku;

    private String name;

    private Long quantity;

    private String category;

}
