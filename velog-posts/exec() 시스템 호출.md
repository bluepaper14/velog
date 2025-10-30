# exec() 시스템 호출

<h3 id="exec의-개념">exec()의 개념</h3>
<p>exec()는 현재 프로세스의 메모리 공간을 새로운 프로그램으로 대체하는 함수 호출이다. 즉 새 프로그램을 현재 프로세스에서 실행시킨다. exec()계열 함수는 여러가지가 있다. 그중 path 검색이 되는 execvp()에 대해 자세히 알아보자.</p>
<h3 id="exec-기본형">exec() 기본형</h3>
<p>예제를 보자.</p>
<pre><code class="language-c">// exec_sam.c
#include &lt;unistd.h&gt;   // execvp() 사용을 위해 필요
#include &lt;stdio.h&gt;    // printf() 사용
#include &lt;stdlib.h&gt;   // exit() 사용

int main() {
    // 실행할 프로그램과 인자 설정
    char *args[] = {&quot;./sam.out&quot;, NULL};

    // execvp(프로그램 이름, 인자 목록)
    execvp(&quot;./sam.out&quot;, args);

    // execvp가 실패하면 아래 코드 실행됨
    perror(&quot;execvp 실패&quot;); // 오류 출력
    exit(1);
}
</code></pre>
<p>위 프로그램(exec_sam.c)는 자신이 아닌 sam.out을 실행하도록 하는 프로그램이다. 자신을 sam으로 바꿔치기 하는 역할을 한다. 호출에 성공하면 절대 복귀하지 않는다</p>
<p>그리고 execvp()가 실패한 경우에만 perror()가 실행되어 오류 메시지가 출력된다. 이는 execvp()가 성공하면 현재 프로세스의 코드 자체가 완전히 다른 프로그램으로 바뀌어 이후의 코드를 더 이상 실행할 수 없기 때문이다.</p>
<h3 id="예제1---파일-호출">예제1 - 파일 호출</h3>
<pre><code class="language-c">#include &lt;stdio.h&gt;
#include &lt;unistd.h&gt; // execvp() 사용을 위해 필요
#include &lt;stdlib.h&gt; // exit(), EXIT_FAILURE 사용

int main() {
    // 1️⃣ 실행할 프로그램 파일 정의
    // execvp()는 PATH에서 파일을 검색하지만, 현재 디렉터리를 사용하려면 './' 포함
    const char *file = &quot;./sam.out&quot;;

    // 2️⃣ 실행할 프로그램에 전달할 인자 배열 정의
    // argv[0]은 항상 프로그램 이름
    char *const argv_list[] = {
        (char *)&quot;sam.out&quot;, // argv[0]: 프로그램 이름
        (char *)&quot;인자1&quot;,   // argv[1]: 첫 번째 인자
        (char *)&quot;인자2&quot;,   // argv[2]: 두 번째 인자
        (char *)NULL       // 배열 끝 표시 (필수)
    };

    // 3️⃣ execvp() 호출 전 메시지 출력
    printf(&quot;... execvp() 실행 전: 현재 프로세스에서 출력 ...\n&quot;);
    printf(&quot;이제 execvp()를 사용해 PATH에서 ./sam.out 프로그램을 실행합니다.\n\n&quot;);

    // 4️⃣ execvp() 호출
    // 성공하면 현재 프로세스가 sam.out으로 완전히 교체됨
    if (execvp(file, argv_list) == -1) {
        // execvp() 실패 시에만 이 코드 실행
        perror(&quot;execvp() 실행 오류&quot;);
        exit(EXIT_FAILURE);
    }

    // 5️⃣ 성공하면 절대 도달하지 않는 코드
    printf(&quot;... 이 메시지는 출력되지 않아야 합니다. (실패 시에만 출력) ---\n&quot;);
    return 0;
}</code></pre>
<p>위 코드는 ./sam.out이 하드코딩되어 고정적으로 실행된다.</p>
<h3 id="예제2---파일-호출--경로-검색">예제2 - 파일 호출 + 경로 검색</h3>
<pre><code class="language-c">#include &lt;stdio.h&gt;
#include &lt;unistd.h&gt;  // execvp() 사용을 위해 필요
#include &lt;stdlib.h&gt;  // exit(), EXIT_FAILURE 사용

int main(int argc, char *argv[]) {
    // 1️⃣ 명령행 인자로 실행할 프로그램 받기
    if (argc &lt; 2) {
        fprintf(stderr, &quot;사용법: %s &lt;실행할_프로그램_경로&gt;\n&quot;, argv[0]);
        exit(EXIT_FAILURE);  // 프로그램 종료
    }

    // 2️⃣ 실행할 프로그램 파일 경로 지정
    const char *file = argv[1];

    // 3️⃣ 실행할 프로그램에 전달할 인자 배열 설정
    // argv[0] : 프로그램 이름, 이후 argv[1..n] : 실행 인자
    char *const argv_list[] = {
        (char *)file,      // argv[0]: 프로그램 이름
        (char *)&quot;인자1&quot;,    // argv[1]: 예제 인자1
        (char *)&quot;인자2&quot;,    // argv[2]: 예제 인자2
        NULL               // 배열 끝 표시 (필수)
    };

    // 4️⃣ execvp() 호출 전 메시지 출력
    printf(&quot;... execvp() 실행 전: 현재 프로세스에서 출력 ...\n&quot;);
    printf(&quot;이제 execvp()를 사용하여 '%s' 프로그램을 실행합니다.\n\n&quot;, file);

    // 5️⃣ execvp() 호출
    // 성공하면 현재 프로세스가 완전히 'file' 프로그램으로 교체됨
    if (execvp(file, argv_list) == -1) {
        // execvp() 실패 시에만 실행
        perror(&quot;execvp() 실행 오류&quot;);
        exit(EXIT_FAILURE);  // 오류 발생 시 종료
    }

    // 6️⃣ execvp() 성공 시 절대 도달하지 않는 코드
    printf(&quot;... 이 메시지는 출력되지 않아야 합니다. ---\n&quot;);
    return 0;
}
</code></pre>
<p>두번째 코드는 첫번째 코드와 달리 실행할 프로그램을 지정할 수 있다.</p>
<pre><code class="language-c">const char *file = argv[1];</code></pre>
<p>실행할 프로그램 경로를 명령행 인자로 받는다.</p>
<pre><code class="language-bash">./exec_sam.out ./sam.out</code></pre>
<p>argv[0] → 현재 실행 중인 프로그램 (exec_sam.out)
argv[1] → 명령행으로 전달한 실행 대상 프로그램 (sam.out)
다음엔 exec()와 fork()에 대한 프로세스 관점으로 차이점을 알아보자.</p>