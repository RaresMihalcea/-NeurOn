import { Component } from '@angular/core';
import { IpcService } from './services/ipc.service';

@Component({
	selector: 'app-root',
	templateUrl: './app.component.html',
	styleUrls: ['./app.component.scss']
})
export class AppComponent {
	title = 'NeurOn';
	constructor(public ipcService: IpcService) {
		this.ipcService.send()
	}


}
