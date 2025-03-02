import { ImaVidState } from "../../state";
import { BaseElement } from "../base";
import { lookerLoader } from "../common/looker.module.css";

export class LoaderBar extends BaseElement<ImaVidState> {
  private buffering = false;

  isShown({ thumbnail }: Readonly<ImaVidState["config"]>) {
    return thumbnail;
  }

  createHTMLElement() {
    const element = document.createElement("div");
    element.classList.add(lookerLoader);
    element.innerText = "loaderbar";
    element.attributes["data-cy"] = "imavid-loader-bar";
    return element;
  }

  renderSelf({ buffering, hovering, error }: Readonly<ImaVidState>) {
    this.buffering = buffering && hovering && !error;

    if (this.buffering) {
      this.element.style.display = "block";
    } else {
      this.element.style.display = "none";
    }
    return this.element;
  }
}
