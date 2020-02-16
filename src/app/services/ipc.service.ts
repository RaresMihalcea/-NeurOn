import { Injectable } from '@angular/core';
import { IpcRenderer } from 'electron';

declare var electron: any;

@Injectable({
	providedIn: 'root'
})
export class IpcService {
	private _ipc: IpcRenderer | undefined;
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

	public send() {
		this._ipc.on('testIpc', (event, data) => console.log(data))
		this._ipc.send('test', 'ping');
	}



	//   componentDidMount() {
	//     ipcRenderer.on('testIpc', this.handleRenderer.bind(this));
	//     ipcRenderer.send('test', 'ping');
	// }

	// componentWillUnmount() {
	//     ipcRenderer.removeListener('testIpc', this.handleRenderer.bind(this));
	// }

}
