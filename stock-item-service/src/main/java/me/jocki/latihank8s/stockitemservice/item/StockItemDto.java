package me.jocki.latihank8s.stockitemservice.item;

import lombok.Data;

import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.PositiveOrZero;

@Data
public class StockItemDto {

    public StockItemDto(StockItem stockItem) {
        this.sku = stockItem.getSku();
        this.name = stockItem.getName();
        this.quantity = stockItem.getQuantity();
        this.category = stockItem.getCategory();
    }

    @NotBlank
    private String sku;

    @NotBlank
    private String name;

    @PositiveOrZero
    @NotNull
    private Long quantity;

    @NotBlank
    private String category;

}
