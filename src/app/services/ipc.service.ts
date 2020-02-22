import { Injectable } from '@angular/core';
import { IpcRenderer } from 'electron';

declare var electron: any;

@Injectable({
	providedIn: 'root'
})
export class IpcService {
	private _ipc: IpcRenderer | undefined;
	isAlreadyRunning = false;
	finished = false;

	constructor() {
		if (window.require) {
			try {
				this._ipc = window.require('electron').ipcRenderer;
			} catch (e) {
				throw e;
			}
		} else {
			console.warn('Electron\'s IPC was not loaded');
		}
	}

	public send(data) {
		this._ipc.on('error', (event, data) => console.log(data));
		this._ipc.on('info', (event, data) => {
			console.log(data);
			if(data == 'Algorithm is already running') {
				console.log('hello');
				this.isAlreadyRunning = true;
			}
			if(data == 'Algorithm Finished') {
				this.finished = true;
			}
		});
		this._ipc.send('run', data);
		this.finished = false;
	}



	//   componentDidMount() {
	//     ipcRenderer.on('testIpc', this.handleRenderer.bind(this));
	//     ipcRenderer.send('test', 'ping');
	// }

	// componentWillUnmount() {
	//     ipcRenderer.removeListener('testIpc', this.handleRenderer.bind(this));
	// }

}
