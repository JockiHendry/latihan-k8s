import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ImageUploadComponent } from './image-upload/image-upload.component';
import {MatButtonModule} from '@angular/material/button';
import {MatProgressBarModule} from '@angular/material/progress-bar';
import { ImageComponent } from './image/image.component';


@NgModule({
    imports: [
        CommonModule,
        MatButtonModule,
        MatProgressBarModule,
    ],
    exports: [
        ImageUploadComponent,
        ImageComponent
    ],
  declarations: [
    ImageUploadComponent,
    ImageComponent
  ]
})
export class SharedModule { }
