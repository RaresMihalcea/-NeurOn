import { Component, OnInit, NgZone, ViewChild } from '@angular/core';
import { CdkTextareaAutosize } from '@angular/cdk/text-field';
import {take} from 'rxjs/operators';

@Component({
	selector: 'app-matrix',
	templateUrl: './matrix.component.html',
	styleUrls: ['./matrix.component.scss']
})
export class MatrixComponent implements OnInit {

	constructor(private _ngZone: NgZone) {}

	ngOnInit() {}

	@ViewChild('autosize') autosize: CdkTextareaAutosize;
  
	triggerResize() {
	  // Wait for changes to be applied, then trigger textarea resize.
	  this._ngZone.onStable.pipe(take(1))
		  .subscribe(() => this.autosize.resizeToFitContent(true));
	}

}
