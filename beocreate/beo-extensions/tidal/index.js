/*Copyright 2019 Bang & Olufsen A/S
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.*/

// tidal CONTROL FOR BEOCREATE

console.log('TIDAL FILE INCLUDED');

var exec = require("child_process").exec;
var fs = require("fs");

	var debug = beo.debug;
	var version = require("./package.json").version;
	
	
	var sources = null;
	
	var settings = {
		tidalEnabled: true,
		loggedInAs: false
	};
	var configuration = {};
	
	beo.bus.on('general', function(event) {
            console.log('beo.bus.on(general)');		
		if (event.header == "startup") {
			
                        console.log('startup');		
			if (beo.extensions.sources &&
				beo.extensions.sources.setSourceOptions &&
				beo.extensions.sources.sourceDeactivated) {
				sources = beo.extensions.sources;
			}
			
			if (sources) {
				gettidalStatus(function(enabled) {
					sources.setSourceOptions("tidal", {
						enabled: enabled,
						transportControls: true,
						usesHifiberryControl: true,
						aka: "tidal"
					});
				});
			}
			
			// Check login here (removed).
			if (sources && Object.keys(configuration).length == 0) {
				sources.setSourceOptions("tidal", {
					enabled: true
				});
			}
		}
		
		if (event.header == "activatedExtension") {
                        console.log('activatedExtension');		
			if (event.content.extension == "tidal") {
				beo.bus.emit("ui", {target: "tidal", header: "tidalSettings", content: settings});
			}
		}
	});
	
	beo.bus.on('product-information', function(event) {
                console.log('product-information');		
		if (event.header == "systemNameChanged") {
			// Listen to changes in system name and update the tidal display name.
			if (event.content.systemName) {
				configure({section: "Authentication", option: "device-name", value: ("'"+event.content.systemName.split(" ").join("-")+"'")}, true);
			}
			
		}
		
		
	});
	
	beo.bus.on('tidal', function(event) {
                console.log(' beo.bus.on(tidal)');
		if (event.header == "tidalEnabled") {
		        console.log('tidalEnabled');	
			if (event.content.enabled != undefined) {
				settidalStatus(event.content.enabled, function(newStatus, error) {
					beo.bus.emit("ui", {target: "tidal", header: "tidalSettings", content: settings});
					if (sources) sources.setSourceOptions("tidal", {enabled: newStatus});
					if (newStatus == false) {
						if (sources) sources.sourceDeactivated("tidal");
					}
					if (error) {
						beo.bus.emit("ui", {target: "tidal", header: "errorTogglingtidal", content: {}});
					}
				});
			}
		
		}
		
	});
	
	
	function gettidalStatus(callback) {
            console.log('SERVER gettidalStatus()');
            exec("systemctl is-active --quiet tidal.service").on('exit', function(code) {
               console.log('gettidalStatus code'+ code);
			if (code == 0) {
                                settings.tidalEnabled = true;
				callback(true);
			} else {
                                settings.tidalEnabled = false;
			        callback(false);
			}
            });
            //console.log('HELLO MOTO!');            
            //settings.tidalEnabled = !settings.tidalEnabled;
	}
	
	function settidalStatus(enabled, callback) {
		if (enabled) {
			exec("systemctl enable --now tidal.service").on('exit', function(code) {
				if (code == 0) {
					settings.tidalEnabled = true;
					if (debug) console.log("TIDAL Connect enabled.");
					callback(true);
				} else {
					settings.tidalEnabled = false;
					callback(false, true);
				}
			});
		} else {
			exec("systemctl disable --now tidal.service").on('exit', function(code) {
				settings.tidalEnabled = false;
				if (code == 0) {
					callback(false);
					if (debug) console.log("TIDAL Connect disabled.");
				} else {
					callback(false, true);
				}
			});
		}
            //settings.tidalEnabled = enabled;
            //callback(true);
	}
	
	function configure(options, relaunch, callback) {
	  callback(true);
	}
	
	configModified = 0;
	
module.exports = {
	version: version,
	isEnabled: gettidalStatus
};

