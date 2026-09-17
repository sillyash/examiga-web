<template>
	<footer class="app-footer">
		<p>&copy; {{ new Date().getFullYear() }} EX-AMIGA. All rights reserved.</p>
	</footer>
</template>

<style scoped>
.app-footer {
	padding: 1rem;
	text-align: center;
	border-top: 2px solid var(--color-border);
}

.app-footer p {
	margin: 0;
}
</style>
