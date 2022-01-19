import {Component, Input} from '@angular/core';
import {environment} from '../../../environments/environment';

@Component({
  selector: 'app-image',
  templateUrl: './image.component.html',
  styleUrls: ['./image.component.css'],
})
export class ImageComponent  {

  @Input() width = 200;
  @Input() height = 200;
  @Input() fileServerUrl = environment.fileServerUrl;
  @Input() bucket: string|null = null;
  @Input() filename: string|null = null;

  constructor() { }

  get thumbnailURL(): string|null {
    if (this.filename == null) {
      return null;
    }
    return `${this.fileServerUrl}${this.bucket ? '/' + this.bucket : ''}/thumbnail/${this.filename}`;
  }

  get fileURL(): string|null {
    if (this.filename == null) {
      return null;
    }
    return `${this.fileServerUrl}${this.bucket ? '/' + this.bucket : ''}/${this.filename}`;
  }

}
