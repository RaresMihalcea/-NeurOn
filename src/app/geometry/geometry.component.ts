import { Component, OnInit, NgZone, ViewChild } from '@angular/core';
import { CdkTextareaAutosize } from '@angular/cdk/text-field';
import { take } from 'rxjs/operators';

@Component({
	selector: 'app-geometry',
	templateUrl: './geometry.component.html',
	styleUrls: ['./geometry.component.scss']
})
export class GeometryComponent implements OnInit {

	constructor(private _ngZone: NgZone) {}

	ngOnInit() {}

	@ViewChild('autosize') autosize: CdkTextareaAutosize;
  
	triggerResize() {
	  // Wait for changes to be applied, then trigger textarea resize.
	  this._ngZone.onStable.pipe(take(1))
		  .subscribe(() => this.autosize.resizeToFitContent(true));
	}

}
