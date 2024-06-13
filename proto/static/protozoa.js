
class ProtoView {
    constructor(proto) {
	this.proto = proto;
    }

    show() {
	let box = document.createElement("div");
	box.setAttribute("class", "box")
	box.setAttribute("id", this.proto.tag);

	let header = document.createElement("div");
	header.setAttribute("class", "header");
	header.appendChild(document.createTextNode(this.proto.tag));

	let body = document.createElement("div");
	body.setAttribute("class", "body");

	let close = document.createElement("a");
	close.setAttribute("id", `close-${this.proto.tag}`);
	close.textContent = "Close";

	let slots = document.createElement("ul");
	this.proto.slots.forEach((slotName) => {
	    let slot = document.createElement("li");
	    slot.textContent = slotName;
	    slots.appendChild(slot);
	});
	body.appendChild(close);
	body.appendChild(slots);

	box.appendChild(header);
	box.appendChild(body);
	return box;
    }
}


class Browser {
    displayObjectSlots(tag) {
	document.getElementById("objects").appendChild(view.show());
    }

    browseObject(tag) {
	let options = {
	    method: 'GET',
	};
	fetch(`http://127.0.0.1:5000/describe/${tag}`, options)
	    .then(response => response.json())
	    .then(this.createView)
	    .then(this.show)
	    .catch(err => console.error(err));
    }

    createView(jsonData) {
	console.log(`Creating a view for proto: ${jsonData.tag}`);
	return new ProtoView(jsonData);
    }

    show(view) {
	let viewBox = view.show();
	document.getElementById("objects").appendChild(viewBox);
	document.getElementById(`close-${view.proto.tag}`).addEventListener("click", (el) => {
	    el.preventDefault();
	    document.getElementById(view.proto.tag).remove();
	});
    }
}


class UIManager {
    constructor() {
	this.browser = new Browser();
    }

    bindObjectBrowserLinks() {
	const list = document.getElementsByClassName("object-browser-link");
	for( let i = 0; i < list.length; i++) {
	    this.bindObjectBrowserHandler(list[i]);
	}
    }

    bindObjectBrowserHandler(element) {
	let tag = element.getAttribute("id").replace("open-", "");
	element.addEventListener("click", (el) => {
	    console.log(`binding browseObject to ${tag}`);
	    el.preventDefault();
	    this.browser.browseObject(tag);
	});
    }
}


let ui = new UIManager();
ui.bindObjectBrowserLinks();
