// Read the story, pick what you'd do, and see how the night ends.
const scenes = {
  start: {
    title: "The ride home",
    story: "Last winter, I closed the pharmacy on Grant Street and missed the 2:58. The stop was empty. Then a man came out of the dark end of the car park.",
    choices: [["Keep my distance", "distance"], ["Ask if he knows when the bus is coming", "ask"]]
  },
  distance: {
    title: "Under the shelter light",
    story: "He stayed by the road. His jacket was dry, even though it was raining. I turned my name badge around. He smiled like he'd seen me do it.",
    choices: [["Walk to the all-night shop", "shop"], ["Wait for the bus anyway", "wait"]]
  },
  ask: {
    title: "He knows your name",
    story: "He looked at my badge. 'Maya, right? My sister's just up the road. I'll give you a lift.' I hadn't told him my name. I was wearing it in big blue letters.",
    choices: [["Say no and head for the shop", "shop"], ["Ask him to call the pharmacy first", "call"]]
  },
  shop: {
    title: "Fluorescent lights",
    story: "I walked fast, not running until I reached the open laundrette. The man never followed. The woman folding towels let me use her phone. My manager stayed on the line until my ride arrived.",
    end: true
  },
  wait: {
    title: "2:58 again",
    story: "The bus came with its inside lights off. I stepped back. The man got on. Through the windows, I saw every seat was wet. The driver looked at me and shut the doors.",
    end: true
  },
  call: {
    title: "A familiar voice",
    story: "He called the pharmacy. The night manager answered and said, 'Maya, don't get in a car. I'm coming.' The man stopped smiling. By the time headlights reached the stop, he was gone.",
    end: true
  }
};

let page = 1;
const title = document.querySelector("#title");
const story = document.querySelector("#story");
const choices = document.querySelector("#choices");
const again = document.querySelector("#again");

function show(sceneName) {
  const scene = scenes[sceneName];
  title.textContent = scene.title;
  story.textContent = scene.story;
  document.querySelector("#page").textContent = String(page).padStart(2, "0");
  choices.replaceChildren();

  if (scene.end) {
    again.hidden = false;
    return;
  }

  scene.choices.forEach(([words, next]) => {
    const button = document.createElement("button");
    button.textContent = words;
    button.addEventListener("click", () => {
      page++;
      show(next);
    });
    choices.append(button);
  });
}

again.addEventListener("click", () => {
  page = 1;
  again.hidden = true;
  show("start");
});

show("start");