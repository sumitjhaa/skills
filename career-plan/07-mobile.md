# 📱 Mobile Apps — Baby Style (8-10 weeks)

**For:** No coding experience. Want to build apps. Like the idea of making something people use on their phone.

**Time:** 3 hrs/day | **Goal:** Junior React Native / Flutter developer

**Pay:** $55-85k | **Difficulty:** Medium

---

## Pick One: React Native vs Flutter

| | React Native | Flutter |
|---|---|---|
| Language | JavaScript + TypeScript | Dart |
| More jobs | ✅ Yes (more companies use it) | ❌ Fewer jobs |
| Growing faster | ❌ | ✅ Yes |
| Easier to learn | ✅ (JS skills transfer to web) | ❌ New language |
| **Pick if...** | You want more job options | You like new tech |

> **Not sure? Pick React Native.** More jobs, and you can switch to web dev later with the same skills.

---

## 🗓️ Week 1-2 — Language (pick your path)

### React Native path: Learn JavaScript

**Day 1:** Variables, functions, arrays, if/else — see 03-express-js.md Week 1

**Day 2:** Objects, loops, arrow functions

**Day 3:** Async: promises, async/await

**Day 4:** Git + terminal basics

**Day 5-7:** Build a CLI todo app in JS

### Flutter path: Learn Dart

**Day 1:** What is Dart?
- Variables: `var name = "Alex"`, `int age = 25`
- Functions: `int double(int n) => n * 2`

**Do:** Print your name, age, and a calculation.

**Day 2:** Lists + Loops
- `var colors = ["red", "blue"]`
- `for (var c in colors) { print(c); }`

**Do:** Make a list of 5 things. Loop through and print each.

**Day 3:** Classes + null safety
- `class Person { String? name; int? age; }`
- `?` means it can be null

**Do:** Make a Person class. Create 2 people. Print their names.

**Day 4:** Async in Dart
- `Future`, `async`, `await`
- `await Future.delayed(Duration(seconds: 2))`

**Do:** Write a function that waits 2 seconds and then prints "Done".

**Day 5-7:** Practice
- Build a CLI todo app in Dart

---

## 🗓️ Week 3 — Your First App

### React Native

**Day 1:** Setup
- `npx react-native init MyApp`
- Or use Expo (easier): `npx create-expo-app MyApp`
- Run on phone (Expo Go app) or emulator

**Do:** Get "Hello World" showing on your phone. 🎉

**Day 2:** Core components
- `View` = container (like `<div>`)
- `Text` = text
- `Image` = image
- `ScrollView` = scrollable page

**Do:** Make a screen with title, subtitle, and an image.

**Day 3:** Styling
- `style={{ color: 'blue', fontSize: 20 }}`
- Flexbox for layout

**Do:** Center everything on the screen. Make a card with shadow.

**Day 4:** State + Pressable
- `const [count, setCount] = useState(0)`
- `<Pressable onPress={() => setCount(count + 1)}>`

**Do:** Build a tap counter. Show how many times you tapped.

**Day 5:** Lists (FlatList)
- `FlatList` = scrollable list of items
- `data={items}` `renderItem={({item}) => <Text>{item.name}</Text>}`

**Do:** Show a list of 10 items with FlatList.

**Day 6-7:** Navigation
- React Navigation: stack navigator (screen A → screen B)
- `navigation.navigate("Details", { id: 1 })`

**Do:** Make 2 screens. Navigate between them. Pass data.

---

### Flutter path (parallel to above)

**Day 1:** Setup
- Install Flutter SDK
- `flutter create my_app`
- Run on emulator or phone

**Do:** Get the default Flutter counter app running.

**Day 2:** Widgets
- Everything is a widget (like LEGO blocks)
- `Text()`, `Container()`, `Row()`, `Column()`, `Image()`

**Do:** Make a screen with title, subtitle, and image.

**Day 3:** Layout
- `Center()`, `Padding()`, `EdgeInsets`, `SizedBox`
- `Row` (horizontal), `Column` (vertical)

**Do:** Make a card with rounded corners and shadow.

**Day 4:** State + Buttons
- `StatefulWidget` + `setState()`
- `ElevatedButton(onPressed: () { setState(() { count++ }); })`

**Do:** Build a tap counter.

**Day 5:** Lists (ListView)
- `ListView.builder(itemCount: 10, itemBuilder: (ctx, i) => Text("Item $i"))`

**Do:** Show a list of 10 items.

**Day 6-7:** Navigation
- `Navigator.push(MaterialPageRoute(builder: (ctx) => DetailsScreen()))`
- Pass data between screens

**Do:** Make 2 screens. Navigate. Pass data.

---

## 🗓️ Week 4 — Real App Features

### Day 1-2: API calls
- Fetch data from internet
- `fetch("https://api.github.com/users/defunkt")` (RN)
- `http.get(Uri.parse("..."))` (Flutter)
- Show loading spinner while fetching

**Do:** Fetch weather data. Show temperature + city name.

### Day 3-4: Local storage
- Save data on the phone
- AsyncStorage (RN) or SharedPreferences (Flutter)
- Or SQLite for complex data

**Do:** Save user preferences (dark mode, favorite city).

### Day 5-6: Device features
- Camera: take photo
- Location: get user's GPS
- Permissions: ask user before using features

**Do:** Build a screen that shows your current location on a map.

### Day 7: Polish
- App icon
- Splash screen
- Handle errors gracefully (show message, don't crash)

---

## 🗓️ Week 5-6 — Full App

### Build a complete app (pick one):

**Option A: Habit tracker**
```
- Add habits (Drink water, Exercise, Read)
- Check off daily
- Show streak (consecutive days)
- Save locally
- Push notifications reminders
```

**Option B: Recipe app**
```
- Browse recipes from an API
- Search by name/ingredient
- Save favorites
- Shopping list from recipes
```

**Option C: Expense tracker**
```
- Add expenses (amount, category, date)
- Show total by category (pie chart)
- Monthly budget
- Export to CSV
```

**Do:** Build it. Deploy it (TestFlight or Play Store internal testing).

---

## 🗓️ Week 7-8 — Portfolio + Job Hunt

### Day 1-2: Polish app
- App store screenshots
- App description
- GitHub README with screen recording

### Day 3: Resume
- 1 page. App as experience.
- Keywords: React Native or Flutter, APIs, navigation, app store deployment

### Day 4: LinkedIn
- Headline: "Mobile Developer"
- Add app with screenshots

### Day 5-7: Apply
- LinkedIn, Indeed — "Junior React Native Developer" or "Flutter Developer"
- Apply to app development agencies (they hire juniors)
- Also apply to web dev roles (if you learned React Native, you know React)

---

> ✅ **Mobile apps = tangible product you can show.** When you pull out your phone and demo an app YOU built, people are impressed. Interviewers too.
