# Py-Raid

---

## 백문이 불여일견

https://youtu.be/LVGm19sxB-I

## 서두

서울과학기술대학교 2023년도 2학기 OSS term project 과제입니다.

python을 사용하여 제작했습니다,.

numpy, PyQt5, threading등 다양한 라이브러리를 사용하였습니다.

게임 프로젝트임에도 py game을 사용하지 않고 PyQt5를 이용하여 구현하였기 때문에, 최적화가 되어있지 않고 CPU 사양이 좋지 않으면 원활한 진행이 힘들 수 있습니다.

## 본 게임에 대해

### 실행방법

pyRaid.py 파일을 실행하면 됩니다.

나머지 파일들은 전부 레거시데이터 혹은 더미데이터들이니 사용하지 않습니다.

### 조작법

- a: 좌측 이동
- d:우측 이동
- w: 점프

### 목적

거대한 보스의 공격을 피해서, 맵 곳곳에 생성되는 코퍼레이션을 파괴하면 됩니다.

총 5개의 코퍼레이션이 생성되고, 하나의 코퍼레이션이 파괴될때마다 게임의 난이도는 상승합니다.

## 개요

이 게임은 Window Kill과 Terraria에 영향을 받아 만들었습니다.

윈도우 킬은 단순한 캐쥬얼 탄막 슈팅 게임입니다. 이 게임은 플레이어의 창이 계속해서 줄어 들고, 다른 창에 있는 적들이 플레이어를 공격한다는 특징이 있습니다.

테라리아는 2D 샌드박스 게임으로, 낮에는 집을 짓고 밤에는 차례로 나타나는 보스를 섬멸하는 것이 목표입니다.

이 두 게임에서 아이디어를 얻어 게임 기획을 시작하였습니다.

중력이 작용하는 2D 화면의 게임에서 창밖에 존재하는 보스의 공격을 피하며 살아남는 것이 이 게임의 목적입니다.

![Untitled](https://img.itch.zone/aW1nLzEzNjAwNTE2LnBuZw==/original/bjfxV3.png)

![Untitled](https://static.wikia.nocookie.net/terraria_gamepedia/images/9/90/6yrsparty.png/revision/latest?cb=20170516220438)

## PyQt5

이 게임의 척추는 PyQt5로 이루어져 있습니다.

게임을 만들기에 pyGame라이브러리가 조금 더 적절할 수 있지만, 플레이어, 보스, 발판등의 창들을 관리하고, 외부 모듈 없이 자체적으로 동기적 코드 실행이 가능하다는 장점이 있어 PyQt를 사용하였습니다.

무엇보다 창을 띄우는 라이브러리로 게임을 만든다는 것은 멋있다고 생각합니다.

PyQt는 각 창을 관리합니다. DB로 부터 플레이어, 보스, 발판의 정보를 가져와서 창에 각 객체를 그려냅니다. 뿐만 아니라 피격 판정, 아이템의 생성 및 사용, 탄막의 이동등의 동적 요소들은 PyQt 객체 안에서 정의되며 반복적으로 실행됩니다.

엄밀히는 PyQt를 부모클래스로 하는 새로운 클래스를 정의하였습니다. 이 클래스는 PyQt와 기능적으로 완전히 동일하지만, 게임이 끝나면 창이 사라지는 기능, 데이터베이스에서 그릴 수 있는 객체를 가져와 자기 화면에 출력하는 기능이 추가되어 있습니다.

## DB

플레이어의 체력, 창의 크기, 적의 색, 탄막의 위치등 게임 내부에 필요한 모든 정보를 DB객체에 저장하였습니다. 

사실 처음 게임을 제작할 당시에는 DB가 존재하지 않았습니다. 그러나 많은 수의 발판, 탄막등을 추가하려다 보니, 코드가 난잡해지고 유지가 불가능한 상황을 마주쳤습니다. 이후, 당시까지의 작업을 전부 폐기하고 처음부터 DB를 염두에 두고 코드를 짜기 시작했습니다.

## NumPy

이 2d게임의 다양한 컴포넌트(레이저, 플레이어, 보스, 탄막)이 갖는 물리량은 모두 이차원 벡터로 표현 가능합니다. 

그리고 이것들의 연산을 편리하게 해주는 라이브러리는 NumPy입니다. 위협적인 객체로부터의 플레이어의 거리, 보스가 돌진해야할 방향, 레이저를 쏴야할 방향과 회전에 필요한 토크, 총알의 속도등에 필요한 벡터연산은 이 라이브러리를 기반으로 개발해였습니다.

## pynput

PyQt내부에도 자체적으로 키보드의 입력을 받는 기능이 존재합니다만, 

- 길게 누르면 디바운스가 존재하다 사라짐
- 해당 창에 포커스가 올라가야만 입력을 받을 수 있음

이라는 한계가 명확하게 존재합니다.

따라서 pynput의 키보드 입력을 활용하였습니다. 그러나 여전히 디바운스 문제는 존재했기 때문에, 이를 해결하기 위해 onA, onD등의 bool타입 변수를 이용하여 해결하였습니다. 

이 과정에서 얻은 디바운싱에 대한 통찰력을 바탕으로 플레이어의 히트 판정에 관한 기능을 추가하였습니다.

## Jump!

구현 관련하여 상당히 애를 많이 먹었던 부분입니다.

바닥과 발판이 존재하는 이 게임의 특성상, 점프를 통해 발판에 올라가는 기능이 필수적입니다만, 점.프를 하여 올라가는 중일 때는 발판을 통과해야하며, 떨어지는 중일때에는 발판위에 멈춰야 합니다. 이 단순한 로직을 해결하기 위해 매우 여러개의 bool타입 변수들이 도입 되었고, 발판이 이동하는 기믹이 추가되자 플레이어가 순간이동하는 문제가 발생하기도 하였습니다.(악마는 디테일에 숨어있다 라는 말을 다시한번 실감하였습니다.)

결과적으로 성공적으로 점프 기능을 구현하는데에는 성공하였지만, 이는 매우 복잡한 형태로 코드 내부에 존재하며, 상술할 스파게티 코드라는 문제에도 직면하게 됩니다.

## 아쉬운 점

### 스파게티 코드

이 프로젝트를 처음 진행하게 되었을 때의 저는 아직 깔끔한 코딩에 대한 개념이 부족했습니다.

이후 학습을 계속하면서 간결한 코드의 장점에 대해 알게 되었습니다.

그때 지금까지 짠 코드의 문제점들이 눈에 들어오기 시작했지만, 이미 리펙토링을 하기엔 시간이 절대적으로 부족하다는 아쉬움이 남습니다.

함수 매개인자를 튜플로 넘겨주기, 데이터베이스에 모든 객체가 사용하는 속성(색상 등) 추가하기, 발판을 클래스로 관리하기 등의 바꾸고 싶은 부분은 많지만 이를 진행하지 못하여 아쉬움이 큽니다.

### 공격 패턴의 단조로움

보스가 플레이어를 공격하는 패턴이 몇 없다는것이 큰 아쉬움입니다.

다만 이후에 바닥이 랜덤하게 사라졌다 이동하는 기믹을 넣어 변칙성이 추가되었습니다.

### 추가하지 못한 기능들

게임의 완성도를 높이기 위해 추가하고 싶은 기능들이 몇 있습니다.

- 플레이어가 피격당했을 시 넉백 판정
- 보스의 공격 전 패턴을 유추할 수 있는 사전 동작

이러한 요소들을 도입한다면 게임에 더 몰입 할 수 있을것이라 생각합니다.

### 어째서 pyQt를

개발 중 추가하고 싶은 기능들이 여럿 있었지만 창을 띄우는 것이 목적인 PyQt를 이용했기 때문에 실패하였습니다.

심지어 처음에 장점으로 뽑았던 내부적으로 비동기적인 스텝 처리는 이후에 기능을 추가할때 이상이 생기게 된다는 문제로 변하게 되었습니다.

이러한 문제점들 때문에 그냥 pyGame을 사용했어야 하나 하는 생각이 들었습니다.

다만 창에 그림그리는 툴로 게임을 만들어? 라는 로망을 만족했기 때문에, 후회는 없습니다 :0

## 느낀 점

OSS 기말 프로젝트를 안내받은 날, 

집에서 유튜브를 보다 window kill게임을 발견한 날,

룸메의 제안으로 친구들과 테라리아를 시작한 날,

그 날 이후로 머리속에서만 존재하던 pyRaid의 완성본을 드디어 컴퓨터 안에서 만나 볼 수 있게 되었습니다.

한달 반의 프로젝트의 종지부는 저에게 있어서 꽤나 뿌듯한 경험입니다.

못내 아쉬운 부분도 있지만, 개발자로서의 자부심을 기르기엔 아쉽지 않은 작업이였습니다.

또한, 코드 디자인과 선택한 기술에 대한 고민을 통해 개발자로서의 성장을 경험할 수 있었습니다. 

앞으로 더 많은 프로젝트를 통해 실력을 향상시키고, 높은 수준의 소프트웨어를 개발할 수 있는 능력을 기르고자 합니다.
