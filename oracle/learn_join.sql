-- 이너조인 배우기!
SELECT * FROM BUYTBL b
	INNER JOIN USERTBL u
		ON b.USERID = u.USERID
	WHERE b.USERID = 'JYP';

-- 첫번째만 buytbl.userid 써서 나머지는 추론해서 동글뱅이 뜹니다!
SELECT buytbl.userid, username, prodname, addr, MOBILE1 || MOBILE2
	AS "연락처" FROM BUYTBL
	INNER JOIN USERTBL
		ON buytbl.USERID = usertbl.USERID ;

-- 동글뱅이 없애기 위해서 각각 테이블 명시해주기~!
SELECT buytbl.userid, usertbl.username, buytbl.prodname, usertbl.addr,
usertbl.MOBILE1 || usertbl.MOBILE2
	AS "연락처" FROM BUYTBL
	INNER JOIN USERTBL
		ON buytbl.USERID = usertbl.USERID ;

-- alias 사용하기! >_<
SELECT b.userid, u.username, b.prodname, u.addr,
u.MOBILE1 || u.MOBILE2
	AS "연락처" FROM BUYTBL b
	INNER JOIN USERTBL u
		ON b.USERID = u.USERID ;

-- where을 사용해서 은지원만 골라내기!
SELECT b.userid, u.username, b.prodname, u.addr,
u.MOBILE1 || u.MOBILE2
	AS "연락처" FROM BUYTBL b
	INNER JOIN USERTBL u
		ON b.USERID = u.USERID
	WHERE b.USERID = 'EJW';

-- u.userid 순으로 나열하기!
SELECT u.userid, u.username, b.prodname, u.addr,
u.MOBILE1 || u.MOBILE2
	AS "연락처" FROM BUYTBL b
	INNER JOIN USERTBL u
		ON b.USERID = u.USERID
	ORDER BY u.USERID ;

-- distinct 이용해서 중복제거하기!
SELECT DISTINCT u.userid, u.username, u.addr
FROM BUYTBL b
	INNER JOIN USERTBL u
		ON b.USERID = u.USERID
	ORDER BY u.USERID ;

-- subquery를 충족하는 애들을 표시하세요!
SELECT u.userid, u.username, u.addr
FROM usertbl u
WHERE EXISTS (
	SELECT * FROM BUYTBL b
	WHERE u.USERID = b.USERID );
