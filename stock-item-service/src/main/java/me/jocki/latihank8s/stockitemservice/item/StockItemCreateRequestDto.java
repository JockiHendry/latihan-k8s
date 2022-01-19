package me.jocki.latihank8s.stockitemservice.item;

import lombok.AllArgsConstructor;
import lombok.Data;

import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.PositiveOrZero;

@Data @AllArgsConstructor
public class StockItemCreateRequestDto {

    @NotBlank
    private String sku;

    @NotBlank
    private String name;

    private String itemImage;

    @PositiveOrZero
    @NotNull
    private Long quantity;

    @NotBlank
    private String category;

}
