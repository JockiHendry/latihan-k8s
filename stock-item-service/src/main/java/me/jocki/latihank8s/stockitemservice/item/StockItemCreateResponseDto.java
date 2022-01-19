package me.jocki.latihank8s.stockitemservice.item;

import lombok.Data;
import lombok.NoArgsConstructor;

import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;

@Data @NoArgsConstructor
public class StockItemCreateResponseDto {

    public StockItemCreateResponseDto(StockItem stockItem) {
        this.sku = stockItem.getSku();
        this.name = stockItem.getName();
        this.itemImage = stockItem.getItemImage();
        this.quantity = stockItem.getQuantity();
        this.category = stockItem.getCategory();
    }

    @NotBlank
    private String sku;

    @NotBlank
    private String name;

    private String itemImage;

    @NotNull
    private Long quantity;

    @NotBlank
    private String category;

}
